from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "OMCF_Runtime"
MCP_ROOT = REPO_ROOT / "MCP"
PROVIDERS_ROOT = RUNTIME_ROOT / "providers"
APPROVAL_POLICY_PATH = RUNTIME_ROOT / "audit" / "human_approval_policy.json"
HUMAN_QUEUE_DIR = RUNTIME_ROOT / "audit" / "human_queue"
METRICS_DIR = RUNTIME_ROOT / "runtime" / "metrics"
METRICS_LOCK_PATH = METRICS_DIR / ".metrics.lock"


REQUIRED_AGENTS = [
    "nuwa.yaml",
    "zhuge_liang.yaml",
    "mozi.yaml",
    "yingzheng.yaml",
    "zhaoyun.yaml",
]

REQUIRED_MCP_FILES = [
    "README.md",
    "PROJECT_PACK_TEMPLATE.md",
    "TASK_CARD_TEMPLATE.md",
    "TASK_FLOW.md",
    "AUDIT_GATE_RULES.md",
    "20_Expert_Training/capability_matrix.md",
    "20_Expert_Training/knowledge_certification.md",
    "16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md",
    "17_Memory_Center/decision_registry.md",
]


@dataclass
class AgentSpec:
    id: str
    name: str
    nickname: str
    role: str
    responsibility: str
    capabilities: list[str]
    knowledge: list[str]
    outputs: list[str]


@dataclass
class ToolSpec:
    id: str
    name: str
    category: str
    provider: str
    description: str
    enabled: bool
    requires_human_approval: bool = False
    status: str = "available"
    capabilities: list[str] = field(default_factory=list)


@dataclass
class ToolInvocation:
    id: str
    agent_id: str
    tool_id: str
    action: str
    status: str
    input: dict[str, Any]
    output: dict[str, Any]
    created_at: str


@dataclass
class ProviderSpec:
    id: str
    name: str
    kind: str
    execution_mode: str
    adapter_path: str
    enabled: bool
    requires_human_approval: bool
    status: str
    capabilities: list[str]


@dataclass
class ApprovalRequest:
    id: str
    scope: str
    label: str
    reason: str
    approver: str
    status: str
    created_at: str


@dataclass
class ProviderAdapterResult:
    status: str
    adapter: str
    output: dict[str, Any]


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            data[key] = value if value else []
            continue
    return data


def load_agents() -> dict[str, AgentSpec]:
    agents_dir = RUNTIME_ROOT / "agents"
    agents: dict[str, AgentSpec] = {}
    for filename in REQUIRED_AGENTS:
        path = agents_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing agent spec: {path}")
        raw = parse_simple_yaml(path)
        agent = AgentSpec(
            id=str(raw.get("id", "")),
            name=str(raw.get("name", "")),
            nickname=str(raw.get("nickname", "")),
            role=str(raw.get("role", "")),
            responsibility=str(raw.get("responsibility", "")),
            capabilities=list(raw.get("capabilities", [])),
            knowledge=list(raw.get("knowledge", [])),
            outputs=list(raw.get("outputs", [])),
        )
        agents[agent.id] = agent
    return agents


def load_provider_config() -> dict[str, Any]:
    path = PROVIDERS_ROOT / "providers.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing provider registry: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_provider_registry() -> tuple[dict[str, ProviderSpec], dict[str, dict[str, str]], str]:
    config = load_provider_config()
    providers: dict[str, ProviderSpec] = {}
    for raw in config.get("providers", []):
        provider = ProviderSpec(
            id=str(raw.get("id", "")),
            name=str(raw.get("name", "")),
            kind=str(raw.get("kind", "")),
            execution_mode=str(raw.get("execution_mode", "")),
            adapter_path=str(raw.get("adapter_path", "")),
            enabled=bool(raw.get("enabled", False)),
            requires_human_approval=bool(raw.get("requires_human_approval", False)),
            status=str(raw.get("status", "")),
            capabilities=list(raw.get("capabilities", [])),
        )
        providers[provider.id] = provider
    agent_defaults = {
        str(agent_id): {
            "provider_id": str(value.get("provider_id", config.get("default_provider", ""))),
            "model": str(value.get("model", "")),
        }
        for agent_id, value in config.get("agent_defaults", {}).items()
    }
    return providers, agent_defaults, str(config.get("default_provider", ""))


def load_approval_policy() -> dict[str, Any]:
    if not APPROVAL_POLICY_PATH.exists():
        raise FileNotFoundError(f"Missing human approval policy: {APPROVAL_POLICY_PATH}")
    return json.loads(APPROVAL_POLICY_PATH.read_text(encoding="utf-8"))


def build_tool_registry() -> dict[str, ToolSpec]:
    tools = [
        ToolSpec(
            id="tool.filesystem.artifact_writer",
            name="Artifact Writer",
            category="filesystem",
            provider="local",
            description="Writes runtime artifacts into the current run directory.",
            enabled=True,
            capabilities=["write_runtime_artifact"],
        ),
        ToolSpec(
            id="tool.knowledge.lookup",
            name="Knowledge Lookup",
            category="knowledge",
            provider="local",
            description="Checks and references MCP knowledge documents without mutating them.",
            enabled=True,
            capabilities=["read_mcp_reference", "check_required_knowledge"],
        ),
        ToolSpec(
            id="tool.memory.lookup",
            name="Memory Lookup",
            category="memory",
            provider="local",
            description="Checks global and project memory templates without creating project slots.",
            enabled=True,
            capabilities=["read_memory_reference", "check_project_memory_template"],
        ),
        ToolSpec(
            id="tool.agent.codex_packet",
            name="Codex/GPT Agent Packet",
            category="agent_bridge",
            provider="codex_or_gpt",
            description="Creates an auditable handoff packet for a real Codex/GPT agent call.",
            enabled=True,
            capabilities=["create_agent_call_packet", "record_agent_input_output_contract"],
        ),
        ToolSpec(
            id="tool.audit.gate",
            name="Audit Gate",
            category="audit",
            provider="local",
            description="Evaluates required runtime gates and records PASS/FAIL status.",
            enabled=True,
            capabilities=["runtime_audit", "gate_validation"],
        ),
        ToolSpec(
            id="tool.provider.invoke",
            name="Provider Invoke",
            category="provider",
            provider="runtime",
            description="Routes agent call packets to a configured provider contract.",
            enabled=True,
            capabilities=["provider_routing", "adapter_contract"],
        ),
        ToolSpec(
            id="tool.approval.request",
            name="Human Approval Request",
            category="approval",
            provider="runtime",
            description="Creates WAIT_HUMAN_APPROVAL records for protected scopes.",
            enabled=True,
            requires_human_approval=True,
            capabilities=["human_in_the_loop", "approval_gate"],
        ),
        ToolSpec(
            id="tool.github.remote",
            name="GitHub Remote",
            category="external_tool",
            provider="github",
            description="Placeholder for repository, issue, PR, and release operations.",
            enabled=False,
            requires_human_approval=True,
            status="adapter_required",
            capabilities=["git_push", "pr_create", "issue_read"],
        ),
        ToolSpec(
            id="tool.openai.gpt",
            name="GPT Model Adapter",
            category="external_model",
            provider="openai",
            description="Placeholder for future GPT API calls. V2 records the contract only.",
            enabled=False,
            requires_human_approval=True,
            status="adapter_required",
            capabilities=["llm_inference", "agent_reasoning"],
        ),
        ToolSpec(
            id="tool.aoem.runtime",
            name="AOEM Runtime Adapter",
            category="external_runtime",
            provider="aoem",
            description="Placeholder for future AOEM execution, GPU scheduling, and privacy compute.",
            enabled=False,
            requires_human_approval=True,
            status="adapter_required",
            capabilities=["aoem_execute", "gpu_dispatch", "privacy_compute"],
        ),
    ]
    return {tool.id: tool for tool in tools}


def check_required_files() -> list[str]:
    missing: list[str] = []
    for rel in REQUIRED_MCP_FILES:
        if not (MCP_ROOT / rel).exists():
            missing.append(f"MCP/{rel}")
    return missing


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def safe_project_code(project_code: str) -> str:
    code = re.sub(r"[^A-Za-z0-9_.-]+", "_", project_code.strip())
    return code.strip("._-") or "project"


def rel_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_local_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@contextmanager
def file_lock(path: Path, timeout_seconds: float = 5.0):
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout_seconds
    fd: int | None = None
    while True:
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("utf-8"))
            break
        except FileExistsError:
            if time.time() >= deadline:
                raise TimeoutError(f"Could not acquire lock: {path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def agent_summary(agents: dict[str, AgentSpec]) -> dict[str, dict[str, Any]]:
    return {
        agent_id: {
            "name": agent.name,
            "nickname": agent.nickname,
            "role": agent.role,
            "capabilities": agent.capabilities,
        }
        for agent_id, agent in agents.items()
    }


def tool_summary(tools: dict[str, ToolSpec]) -> dict[str, dict[str, Any]]:
    return {
        tool_id: {
            "name": tool.name,
            "category": tool.category,
            "provider": tool.provider,
            "enabled": tool.enabled,
            "requires_human_approval": tool.requires_human_approval,
            "status": tool.status,
            "capabilities": tool.capabilities,
        }
        for tool_id, tool in tools.items()
    }


def provider_summary(providers: dict[str, ProviderSpec]) -> dict[str, dict[str, Any]]:
    return {
        provider_id: {
            "name": provider.name,
            "kind": provider.kind,
            "execution_mode": provider.execution_mode,
            "adapter_path": provider.adapter_path,
            "enabled": provider.enabled,
            "requires_human_approval": provider.requires_human_approval,
            "status": provider.status,
            "capabilities": provider.capabilities,
        }
        for provider_id, provider in providers.items()
    }


def build_runtime_context(
    runtime_version: str,
    project_name: str,
    project_code: str,
    project_type: str,
    agents: dict[str, AgentSpec],
    tools: dict[str, ToolSpec] | None = None,
    providers: dict[str, ProviderSpec] | None = None,
) -> dict[str, Any]:
    context: dict[str, Any] = {
        "runtime": runtime_version,
        "created_at": now_iso(),
        "project": {
            "name": project_name,
            "code": project_code,
            "type": project_type,
            "phase": "Phase-1 文档建设",
        },
        "chain": [
            "CAIO-001",
            "PM-001",
            "ARC-001",
            "DOC-001",
            "AUD-001",
        ],
        "agents": agent_summary(agents),
        "gates": {
            "capability_matrix": "MCP/20_Expert_Training/capability_matrix.md",
            "knowledge_certification": "MCP/20_Expert_Training/knowledge_certification.md",
            "aoem_constitution": "MCP/16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md",
            "decision_registry": "MCP/17_Memory_Center/decision_registry.md",
        },
    }
    if tools is not None:
        context["tools"] = tool_summary(tools)
    if providers is not None:
        context["providers"] = provider_summary(providers)
    return context


def new_invocation(
    index: int,
    agent_id: str,
    tool_id: str,
    action: str,
    status: str,
    input_payload: dict[str, Any],
    output_payload: dict[str, Any],
) -> ToolInvocation:
    return ToolInvocation(
        id=f"INV-{index:03d}",
        agent_id=agent_id,
        tool_id=tool_id,
        action=action,
        status=status,
        input=input_payload,
        output=output_payload,
        created_at=now_iso(),
    )


def knowledge_lookup_invocations(start_index: int) -> list[ToolInvocation]:
    rows: list[ToolInvocation] = []
    for offset, rel in enumerate(REQUIRED_MCP_FILES):
        path = MCP_ROOT / rel
        rows.append(
            new_invocation(
                start_index + offset,
                "CAIO-001",
                "tool.knowledge.lookup",
                "check_mcp_reference",
                "SUCCESS" if path.exists() else "FAIL",
                {"path": f"MCP/{rel}"},
                {
                    "exists": path.exists(),
                    "relative_path": f"MCP/{rel}",
                    "size_bytes": path.stat().st_size if path.exists() else 0,
                },
            )
        )
    return rows


def memory_lookup_invocation(index: int) -> ToolInvocation:
    template = MCP_ROOT / "17_Memory_Center" / "Project_Memory" / "PROJECT_MEMORY_TEMPLATE.md"
    project_memory = MCP_ROOT / "17_Memory_Center" / "Project_Memory"
    project_slots = [
        item.name
        for item in project_memory.iterdir()
        if item.is_dir() and not item.name.startswith(".")
    ] if project_memory.exists() else []
    forbidden_slots = {"WPF", "NOVOVM", "Wallet", "Official_Website"}
    forbidden_existing = sorted(slot for slot in project_slots if slot in forbidden_slots)
    slots_without_readme = sorted(
        slot
        for slot in project_slots
        if not (project_memory / slot / "README.md").exists()
    )
    status = "SUCCESS" if template.exists() and not forbidden_existing and not slots_without_readme else "FAIL"
    return new_invocation(
        index,
        "CAIO-001",
        "tool.memory.lookup",
        "check_project_memory_template",
        status,
        {"template": rel_path(template)},
        {
            "template_exists": template.exists(),
            "project_slots": project_slots,
            "forbidden_project_slots": forbidden_existing,
            "slots_without_readme": slots_without_readme,
            "policy": "Project_Memory keeps only the template plus explicitly started project memories with README evidence. Forbidden placeholder slots are not allowed.",
        },
    )


def agent_packet_invocation(
    index: int,
    agent: AgentSpec,
    objective: str,
    required_inputs: list[str],
    expected_outputs: list[str],
    provider_assignment: dict[str, str] | None = None,
) -> ToolInvocation:
    assignment = provider_assignment or {"provider_id": "provider.codex.manual", "model": "codex-current"}
    return new_invocation(
        index,
        agent.id,
        "tool.agent.codex_packet",
        "create_agent_call_packet",
        "READY_FOR_EXTERNAL_AGENT",
        {
            "agent_id": agent.id,
            "agent_name": agent.name,
            "nickname": agent.nickname,
            "objective": objective,
            "required_inputs": required_inputs,
        },
        {
            "expected_outputs": expected_outputs,
            "adapter": "provider_layer",
            "provider_id": assignment.get("provider_id", ""),
            "model": assignment.get("model", ""),
            "execution_note": "Runtime records the call contract. A provider adapter can execute it later.",
        },
    )


def provider_invoke_invocation(
    index: int,
    agent_packet: ToolInvocation,
    providers: dict[str, ProviderSpec],
) -> ToolInvocation:
    provider_id = str(agent_packet.output.get("provider_id", ""))
    provider = providers.get(provider_id)
    if provider is None:
        status = "FAIL"
        provider_payload: dict[str, Any] = {
            "provider_id": provider_id,
            "error": "provider_not_registered",
        }
    elif provider.enabled:
        status = "READY_FOR_PROVIDER"
        provider_payload = {
            "provider_id": provider.id,
            "provider_name": provider.name,
            "execution_mode": provider.execution_mode,
            "requires_human_approval": provider.requires_human_approval,
            "adapter_status": provider.status,
        }
    else:
        status = "WAIT_ADAPTER_CONFIGURATION"
        provider_payload = {
            "provider_id": provider.id,
            "provider_name": provider.name,
            "execution_mode": provider.execution_mode,
            "requires_human_approval": provider.requires_human_approval,
            "adapter_status": provider.status,
        }
    return new_invocation(
        index,
        agent_packet.agent_id,
        "tool.provider.invoke",
        "route_agent_packet_to_provider",
        status,
        {
            "agent_packet_id": agent_packet.id,
            "agent_id": agent_packet.agent_id,
            "provider_id": provider_id,
            "model": agent_packet.output.get("model", ""),
            "objective": agent_packet.input.get("objective", ""),
        },
        provider_payload,
    )


def execute_provider_adapter(agent_packet: ToolInvocation, provider: ProviderSpec) -> ProviderAdapterResult:
    if not provider.enabled:
        return ProviderAdapterResult(
            status="WAIT_ADAPTER_CONFIGURATION",
            adapter=provider.execution_mode,
            output={
                "provider_id": provider.id,
                "provider_name": provider.name,
                "reason": "Provider adapter is registered but disabled.",
            },
        )

    if provider.id == "provider.codex":
        return ProviderAdapterResult(
            status="READY_FOR_CODEX_ADAPTER",
            adapter="providers.codex.codex_cli",
            output={
                "provider_id": provider.id,
                "provider_name": provider.name,
                "execution_mode": provider.execution_mode,
                "agent_packet_id": agent_packet.id,
                "agent_id": agent_packet.agent_id,
                "result_summary": "Codex CLI adapter is available. Use runtime command invoke-codex with a task file for real execution.",
                "runtime_command": "python OMCF_Runtime/runtime/omcf_runtime.py invoke-codex --task-file <task.json> --output-dir <dir>",
                "audit_required": True,
            },
        )

    if provider.id == "provider.codex.manual":
        return ProviderAdapterResult(
            status="PROVIDER_EXECUTED",
            adapter="providers.codex.manual",
            output={
                "provider_id": provider.id,
                "provider_name": provider.name,
                "execution_mode": provider.execution_mode,
                "agent_packet_id": agent_packet.id,
                "agent_id": agent_packet.agent_id,
                "result_summary": "Manual Codex provider accepted the agent packet and produced an auditable execution result.",
                "result_contract": {
                    "objective": agent_packet.input.get("objective", ""),
                    "expected_outputs": agent_packet.output.get("expected_outputs", []),
                    "audit_required": True,
                },
            },
        )

    return ProviderAdapterResult(
        status="WAIT_ADAPTER_CONFIGURATION",
        adapter=provider.execution_mode,
        output={
            "provider_id": provider.id,
            "provider_name": provider.name,
            "reason": "External adapter implementation or credentials are not configured.",
        },
    )


def provider_execute_invocation(
    index: int,
    agent_packet: ToolInvocation,
    providers: dict[str, ProviderSpec],
) -> ToolInvocation:
    provider_id = str(agent_packet.output.get("provider_id", ""))
    provider = providers.get(provider_id)
    if provider is None:
        return new_invocation(
            index,
            agent_packet.agent_id,
            "tool.provider.invoke",
            "execute_provider_adapter",
            "FAIL",
            {
                "agent_packet_id": agent_packet.id,
                "provider_id": provider_id,
            },
            {
                "error": "provider_not_registered",
            },
        )

    result = execute_provider_adapter(agent_packet, provider)
    return new_invocation(
        index,
        agent_packet.agent_id,
        "tool.provider.invoke",
        "execute_provider_adapter",
        result.status,
        {
            "agent_packet_id": agent_packet.id,
            "agent_id": agent_packet.agent_id,
            "provider_id": provider.id,
            "model": agent_packet.output.get("model", ""),
            "objective": agent_packet.input.get("objective", ""),
        },
        {
            "adapter": result.adapter,
            **result.output,
        },
    )


def approval_requests_for_scopes(scopes: list[str]) -> list[ApprovalRequest]:
    policy = load_approval_policy()
    protected_scopes = policy.get("approval_required_scopes", {})
    requests: list[ApprovalRequest] = []
    for index, scope in enumerate(scopes, start=1):
        if scope not in protected_scopes:
            continue
        item = protected_scopes[scope]
        requests.append(
            ApprovalRequest(
                id=f"APR-{index:03d}",
                scope=scope,
                label=str(item.get("label", scope)),
                reason=str(item.get("reason", "")),
                approver=str(policy.get("approver", "King Xu")),
                status=str(policy.get("default_status", "WAIT_HUMAN_APPROVAL")),
                created_at=now_iso(),
            )
        )
    return requests


def approval_invocations(start_index: int, approvals: list[ApprovalRequest]) -> list[ToolInvocation]:
    rows: list[ToolInvocation] = []
    for offset, approval in enumerate(approvals):
        rows.append(
            new_invocation(
                start_index + offset,
                "AUD-001",
                "tool.approval.request",
                "create_human_approval_gate",
                approval.status,
                {
                    "approval_id": approval.id,
                    "scope": approval.scope,
                    "label": approval.label,
                },
                {
                    "approver": approval.approver,
                    "reason": approval.reason,
                    "status": approval.status,
                },
            )
        )
    return rows


def approval_dicts(approvals: list[ApprovalRequest]) -> list[dict[str, Any]]:
    return [
        {
            "id": item.id,
            "scope": item.scope,
            "label": item.label,
            "reason": item.reason,
            "approver": item.approver,
            "status": item.status,
            "created_at": item.created_at,
        }
        for item in approvals
    ]


def write_human_queue_items(run_id: str, project_name: str, approvals: list[ApprovalRequest]) -> list[dict[str, Any]]:
    queue_entries: list[dict[str, Any]] = []
    for approval in approvals:
        filename = f"{run_id}_{approval.id}.json"
        path = HUMAN_QUEUE_DIR / filename
        payload = {
            "queue_id": approval.id,
            "run_id": run_id,
            "project": project_name,
            "task": approval.scope,
            "requester": "AUD-001",
            "approver": approval.approver,
            "runtime_status": approval.status,
            "queue_status": "pending",
            "reason": approval.reason,
            "created_at": approval.created_at,
        }
        write_local_json(path, payload)
        queue_entries.append({**payload, "queue_path": rel_path(path)})
    return queue_entries


def build_metrics_report(
    runtime_version: str,
    run_id: str,
    project_name: str,
    invocations: list[ToolInvocation],
    approvals: list[ApprovalRequest],
    audit_status: str,
) -> dict[str, Any]:
    provider_invocations = [item for item in invocations if item.tool_id == "tool.provider.invoke"]
    provider_success = [item for item in provider_invocations if item.status in {"PROVIDER_EXECUTED", "READY_FOR_PROVIDER"}]
    agent_metrics: dict[str, dict[str, Any]] = {}
    for item in invocations:
        stats = agent_metrics.setdefault(
            item.agent_id,
            {
                "agent_id": item.agent_id,
                "invocations": 0,
                "provider_invocations": 0,
                "provider_executed": 0,
                "approval_requests": 0,
                "failures": 0,
            },
        )
        stats["invocations"] += 1
        if item.tool_id == "tool.provider.invoke":
            stats["provider_invocations"] += 1
        if item.status == "PROVIDER_EXECUTED":
            stats["provider_executed"] += 1
        if item.tool_id == "tool.approval.request":
            stats["approval_requests"] += 1
        if item.status == "FAIL":
            stats["failures"] += 1

    return {
        "runtime": runtime_version,
        "run_id": run_id,
        "project": project_name,
        "created_at": now_iso(),
        "audit_status": audit_status,
        "totals": {
            "tool_invocations": len(invocations),
            "provider_invocations": len(provider_invocations),
            "provider_success": len(provider_success),
            "provider_success_rate": round(len(provider_success) / len(provider_invocations), 4) if provider_invocations else 0,
            "human_approval_requests": len(approvals),
            "human_approval_rate": round(len(approvals) / len(invocations), 4) if invocations else 0,
            "failures": len([item for item in invocations if item.status == "FAIL"]),
        },
        "agent_metrics": agent_metrics,
    }


def update_persistent_metrics(metrics_report: dict[str, Any]) -> list[str]:
    written: list[str] = []
    with file_lock(METRICS_LOCK_PATH):
        for agent_id, current in metrics_report["agent_metrics"].items():
            path = METRICS_DIR / f"{agent_id}.json"
            aggregate = read_json(
                path,
                {
                    "agent_id": agent_id,
                    "runs": 0,
                    "invocations": 0,
                    "provider_invocations": 0,
                    "provider_executed": 0,
                    "approval_requests": 0,
                    "failures": 0,
                    "last_run_id": "",
                    "last_updated": "",
                },
            )
            aggregate["runs"] = int(aggregate.get("runs", 0)) + 1
            for key in ["invocations", "provider_invocations", "provider_executed", "approval_requests", "failures"]:
                aggregate[key] = int(aggregate.get(key, 0)) + int(current.get(key, 0))
            aggregate["provider_success_rate"] = round(
                aggregate["provider_executed"] / aggregate["provider_invocations"], 4
            ) if aggregate["provider_invocations"] else 0
            aggregate["last_run_id"] = metrics_report["run_id"]
            aggregate["last_updated"] = now_iso()
            write_local_json(path, aggregate)
            written.append(rel_path(path))
    return written


def list_local_json_files(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    for item in sorted(path.glob("*.json")):
        payload = read_json(item, {})
        if isinstance(payload, dict):
            payload["_path"] = rel_path(item)
            items.append(payload)
    return items


def audit_invocation(index: int, missing_files: list[str], tool_failures: list[str]) -> ToolInvocation:
    status = "SUCCESS" if not missing_files and not tool_failures else "FAIL"
    return new_invocation(
        index,
        "AUD-001",
        "tool.audit.gate",
        "runtime_v2_gate_check",
        status,
        {
            "required_mcp_files": [f"MCP/{rel}" for rel in REQUIRED_MCP_FILES],
            "checks": ["required_files", "project_memory_template_only", "agent_packets_created"],
        },
        {
            "missing_files": missing_files,
            "tool_failures": tool_failures,
            "audit_result": "PASS" if status == "SUCCESS" else "FAIL",
        },
    )


def audit_invocation_v25(
    index: int,
    missing_files: list[str],
    tool_failures: list[str],
    approvals: list[ApprovalRequest],
) -> ToolInvocation:
    if missing_files or tool_failures:
        status = "FAIL"
        audit_result = "FAIL"
    elif approvals:
        status = "WAIT_HUMAN_APPROVAL"
        audit_result = "WAIT_HUMAN_APPROVAL"
    else:
        status = "SUCCESS"
        audit_result = "PASS"
    return new_invocation(
        index,
        "AUD-001",
        "tool.audit.gate",
        "runtime_v2_5_gate_check",
        status,
        {
            "required_mcp_files": [f"MCP/{rel}" for rel in REQUIRED_MCP_FILES],
            "checks": [
                "required_files",
                "project_memory_template_only",
                "provider_registry",
                "agent_provider_assignments",
                "human_approval_gates",
            ],
        },
        {
            "missing_files": missing_files,
            "tool_failures": tool_failures,
            "approval_requests": [item.id for item in approvals],
            "audit_result": audit_result,
        },
    )


def invocation_dicts(invocations: list[ToolInvocation]) -> list[dict[str, Any]]:
    return [
        {
            "id": item.id,
            "agent_id": item.agent_id,
            "tool_id": item.tool_id,
            "action": item.action,
            "status": item.status,
            "input": item.input,
            "output": item.output,
            "created_at": item.created_at,
        }
        for item in invocations
    ]


def render_nuwa(project_name: str, project_code: str, project_type: str, agent: AgentSpec, runtime_version: str) -> str:
    return f"""
# 01 女娲启动记录

- Agent: {agent.nickname} / {agent.id}
- Runtime: {runtime_version}
- 项目名称: {project_name}
- 项目代号: {project_code}
- 项目类型: {project_type}
- 当前阶段: Phase-1 文档建设

## 启动判断

1. OMCF 制度层已存在。
2. Runtime 进入项目启动链路。
3. 本次运行不写业务代码。
4. Project_Memory 不预设项目槽位，只保留模板。
5. 任务分配必须检查 Capability Matrix 和 Knowledge Certification。

## 调度链路

```text
女娲 -> 诸葛亮 -> 墨子 -> 嬴政 -> 赵云
```
"""


def render_task_tree(project_name: str, project_code: str, agent: AgentSpec) -> str:
    code = project_code.upper()
    return f"""
# 02 诸葛亮任务树

- Agent: {agent.nickname} / {agent.id}
- 项目: {project_name}

## Phase-1 任务树

| 任务编号 | 任务名称 | 责任角色 | 输出物 | 状态 |
|---|---|---|---|---|
| {code}-TASK-001 | 项目资料包确认 | 诸葛亮 | Project Pack Review | READY |
| {code}-TASK-002 | 知识库检索 | 伏羲 | Knowledge Gap Report | READY |
| {code}-TASK-003 | 项目记忆检索 | 仓颉 | Memory Retrieval Report | READY |
| {code}-TASK-004 | 能力矩阵检查 | 诸葛亮 / 赵云 | Capability Gate Report | READY |
| {code}-TASK-005 | 架构树生成 | 墨子 | Architecture Tree | READY |
| {code}-TASK-006 | 文档树生成 | 嬴政 | Document Tree | READY |
| {code}-TASK-007 | 启动审计 | 赵云 | Audit Report | READY |

## 分配原则

1. 不按昵称直接派活，先查能力矩阵。
2. 未认证知识域不得承接生产任务。
3. AOEM 任务必须遵守 AOEM Constitution。
4. 审计失败必须进入 Failure Log。
"""


def render_architecture_tree(project_name: str, project_type: str, agent: AgentSpec) -> str:
    return f"""
# 03 墨子架构树

- Agent: {agent.nickname} / {agent.id}
- 项目: {project_name}
- 项目类型: {project_type}

## 架构树 V1

```text
Project
├── Product Boundary
├── Architecture Boundary
├── Data Boundary
├── API Boundary
├── UI Boundary
├── AI Boundary
├── Server Boundary
├── Audit Boundary
└── Deployment Boundary
```

## 能力门禁

| 门禁 | 状态 | 说明 |
|---|---|---|
| Capability Matrix | REQUIRED | 分配任务前必须检查 |
| Knowledge Certification | REQUIRED | 未认证不得承接生产任务 |
| AOEM Constitution | CONDITIONAL | 涉及 AOEM 时必须检查 |
| Decision Registry | REQUIRED | 重大选择和拒绝方案必须登记 |

## 架构结论

当前仅生成项目启动架构树，不进入业务模块实现。
"""


def render_document_tree(project_name: str, agent: AgentSpec) -> str:
    return f"""
# 04 嬴政文档树

- Agent: {agent.nickname} / {agent.id}
- 项目: {project_name}

## 文档树 V1

```text
Project Documents
├── 00_Project_Charter
├── 01_Product
├── 02_Architecture
├── 03_Database
├── 04_API
├── 05_UI
├── 06_AI
├── 07_Server
├── 08_Test
├── 09_Audit
└── 10_Deployment
```

## Runtime 产物

1. Runtime Context
2. Project Bootstrap
3. Task Tree
4. Architecture Tree
5. Document Tree
6. Audit Report
"""


def render_tool_layer_report(tools: dict[str, ToolSpec], invocations: list[ToolInvocation]) -> str:
    enabled_tools = [tool for tool in tools.values() if tool.enabled]
    disabled_tools = [tool for tool in tools.values() if not tool.enabled]
    invocation_rows = "\n".join(
        f"| {item.id} | {item.agent_id} | {item.tool_id} | {item.action} | {item.status} |"
        for item in invocations
    )
    enabled_rows = "\n".join(
        f"| {tool.id} | {tool.category} | {tool.provider} | {tool.status} |"
        for tool in enabled_tools
    )
    disabled_rows = "\n".join(
        f"| {tool.id} | {tool.category} | {tool.provider} | {tool.status} |"
        for tool in disabled_tools
    )
    return f"""
# 05 Tool Layer Report

Runtime V2 新增工具层。工具层不等于 AI，它负责把 Agent 的意图转换为可审计的工具调用、外部适配器合同和状态记录。

## Enabled Tools

| Tool | Category | Provider | Status |
|---|---|---|---|
{enabled_rows}

## Adapter Required

| Tool | Category | Provider | Status |
|---|---|---|---|
{disabled_rows}

## Invocation Log

| Invocation | Agent | Tool | Action | Status |
|---|---|---|---|---|
{invocation_rows}
"""


def render_provider_execution_plan(providers: dict[str, ProviderSpec], invocations: list[ToolInvocation]) -> str:
    provider_rows = "\n".join(
        f"| {provider.id} | {provider.kind} | {provider.execution_mode} | {provider.adapter_path} | {provider.enabled} | {provider.status} |"
        for provider in providers.values()
    )
    routes = [item for item in invocations if item.tool_id == "tool.provider.invoke"]
    route_rows = "\n".join(
        f"| {item.id} | {item.agent_id} | {item.input.get('provider_id', '')} | {item.input.get('model', '')} | {item.status} |"
        for item in routes
    )
    return f"""
# Provider Execution Plan

Runtime V2.5 separates agent profiles from execution providers.

## Providers

| Provider | Kind | Mode | Adapter Path | Enabled | Status |
|---|---|---|---|---|---|
{provider_rows}

## Agent Routes

| Invocation | Agent | Provider | Model | Status |
|---|---|---|---|---|
{route_rows}
"""


def render_provider_adapter_results(invocations: list[ToolInvocation]) -> str:
    rows = "\n".join(
        f"| {item.id} | {item.agent_id} | {item.input.get('provider_id', '')} | {item.action} | {item.status} |"
        for item in invocations
        if item.tool_id == "tool.provider.invoke"
    )
    return f"""
# Provider Adapter Results

Runtime V2.6 executes enabled provider adapters and records their results.

| Invocation | Agent | Provider | Action | Status |
|---|---|---|---|---|
{rows}
"""


def render_human_approval_report(approvals: list[ApprovalRequest]) -> str:
    if approvals:
        rows = "\n".join(
            f"| {item.id} | {item.scope} | {item.label} | {item.approver} | {item.status} |"
            for item in approvals
        )
    else:
        rows = "| - | - | - | - | NO_APPROVAL_REQUIRED |"
    return f"""
# Human Approval Report

Runtime V2.5 introduces explicit human-in-the-loop gates.

## Approval Requests

| ID | Scope | Label | Approver | Status |
|---|---|---|---|---|
{rows}
"""


def render_metrics_report(metrics_report: dict[str, Any], persistent_metric_paths: list[str]) -> str:
    totals = metrics_report["totals"]
    agent_rows = "\n".join(
        f"| {agent_id} | {item['invocations']} | {item['provider_invocations']} | {item['provider_executed']} | {item['approval_requests']} | {item['failures']} |"
        for agent_id, item in metrics_report["agent_metrics"].items()
    )
    paths = "\n".join(f"- {path}" for path in persistent_metric_paths) if persistent_metric_paths else "- 无"
    return f"""
# Metrics Report

- Runtime: {metrics_report["runtime"]}
- Run ID: {metrics_report["run_id"]}
- Audit Status: {metrics_report["audit_status"]}

## Totals

| Metric | Value |
|---|---|
| Tool Invocations | {totals["tool_invocations"]} |
| Provider Invocations | {totals["provider_invocations"]} |
| Provider Success | {totals["provider_success"]} |
| Provider Success Rate | {totals["provider_success_rate"]} |
| Human Approval Requests | {totals["human_approval_requests"]} |
| Human Approval Rate | {totals["human_approval_rate"]} |
| Failures | {totals["failures"]} |

## Agent Metrics

| Agent | Invocations | Provider Invocations | Provider Executed | Approval Requests | Failures |
|---|---|---|---|---|---|
{agent_rows}

## Persistent Metrics

{paths}
"""


def render_agent_call_packets(invocations: list[ToolInvocation]) -> str:
    packets = [item for item in invocations if item.tool_id == "tool.agent.codex_packet"]
    sections: list[str] = ["# 06 Agent Call Packets"]
    for item in packets:
        inputs = "\n".join(f"- {value}" for value in item.input["required_inputs"])
        outputs = "\n".join(f"- {value}" for value in item.output["expected_outputs"])
        sections.append(
            f"""
## {item.id} / {item.input["nickname"]} / {item.agent_id}

- Adapter: {item.output["adapter"]}
- Provider: {item.output.get("provider_id", "")}
- Model: {item.output.get("model", "")}
- Status: {item.status}

### Objective

{item.input["objective"]}

### Required Inputs

{inputs}

### Expected Outputs

{outputs}

### Guardrails

- 必须引用 Knowledge_Base、Memory_Center 或项目输入资料，不得依赖模型自称记忆。
- 涉及数据结构、银行接口、AI训练数据、AOEM核心执行逻辑时必须进入人工确认。
- 输出必须交给赵云审计。
"""
        )
    return "\n".join(sections)


def render_audit_report(
    project_name: str,
    missing_files: list[str],
    agent: AgentSpec,
    tool_failures: list[str] | None = None,
    approval_requests: list[ApprovalRequest] | None = None,
) -> str:
    failures = tool_failures or []
    approvals = approval_requests or []
    if missing_files or failures:
        status = "FAIL"
    elif approvals:
        status = "WAIT_HUMAN_APPROVAL"
    else:
        status = "PASS"
    missing_text = "\n".join(f"- {item}" for item in missing_files) if missing_files else "- 无"
    failure_text = "\n".join(f"- {item}" for item in failures) if failures else "- 无"
    approval_text = "\n".join(f"- {item.id}: {item.scope} / {item.status}" for item in approvals) if approvals else "- 无"
    if status == "PASS":
        opinion = "启动链路可进入下一步任务规划。"
    elif status == "WAIT_HUMAN_APPROVAL":
        opinion = "启动链路已挂起，等待人工审批后继续。"
    else:
        opinion = "存在关键缺口，不得进入下一步。"
    return f"""
# 赵云启动审计报告

- Agent: {agent.nickname} / {agent.id}
- 项目: {project_name}
- 审计结论: {status}

## 审计范围

1. Agent Registry 完整性。
2. MCP 关键制度文件存在性。
3. Capability Matrix 引用。
4. Knowledge Certification 引用。
5. AOEM Constitution 引用。
6. Decision Registry 引用。
7. Tool Layer 调用记录。

## 缺失文件

{missing_text}

## 工具失败

{failure_text}

## 人工审批

{approval_text}

## 审计意见

{opinion}
"""


def start_project(project_name: str, project_code: str, project_type: str, output_dir: str | None) -> Path:
    agents = load_agents()
    missing_files = check_required_files()
    safe_code = safe_project_code(project_code)
    run_id = f"{safe_code}_{timestamp()}"
    out_dir = Path(output_dir) if output_dir else RUNTIME_ROOT / "tasks" / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    context = build_runtime_context("OMCF_Runtime_V1", project_name, project_code, project_type, agents)
    context["run_id"] = run_id
    context["status"] = "AUDIT_PASS" if not missing_files else "AUDIT_FAIL"

    write_json(out_dir / "00_runtime_context.json", context)
    write_text(out_dir / "01_nuwa_project_bootstrap.md", render_nuwa(project_name, project_code, project_type, agents["CAIO-001"], "OMCF_Runtime_V1"))
    write_text(out_dir / "02_zhuge_task_tree.md", render_task_tree(project_name, safe_code, agents["PM-001"]))
    write_text(out_dir / "03_mozi_architecture_tree.md", render_architecture_tree(project_name, project_type, agents["ARC-001"]))
    write_text(out_dir / "04_yingzheng_document_tree.md", render_document_tree(project_name, agents["DOC-001"]))
    write_text(out_dir / "05_zhaoyun_audit_report.md", render_audit_report(project_name, missing_files, agents["AUD-001"]))

    return out_dir


def build_v2_invocations(
    agents: dict[str, AgentSpec],
    project_name: str,
    project_code: str,
    project_type: str,
    missing_files: list[str],
) -> list[ToolInvocation]:
    invocations = knowledge_lookup_invocations(1)
    next_index = len(invocations) + 1
    invocations.append(memory_lookup_invocation(next_index))
    next_index += 1
    invocations.append(
        agent_packet_invocation(
            next_index,
            agents["PM-001"],
            f"为 {project_name} 生成 Phase-1 任务树，并根据能力矩阵决定责任角色。",
            [
                "MCP/PROJECT_PACK_TEMPLATE.md",
                "MCP/TASK_CARD_TEMPLATE.md",
                "MCP/20_Expert_Training/capability_matrix.md",
            ],
            ["02_zhuge_task_tree.md", "任务依赖与审计门禁"],
        )
    )
    next_index += 1
    invocations.append(
        agent_packet_invocation(
            next_index,
            agents["ARC-001"],
            f"为 {project_name} 生成启动阶段架构树，明确模块边界和禁止编码边界。",
            [
                "02_zhuge_task_tree.md",
                "MCP/02_Architecture/architecture_principles.md",
                "MCP/17_Memory_Center/decision_registry.md",
            ],
            ["03_mozi_architecture_tree.md", "Architecture Decision candidates"],
        )
    )
    next_index += 1
    invocations.append(
        agent_packet_invocation(
            next_index,
            agents["DOC-001"],
            f"为 {project_name} 生成文档树，保持先文档后开发。",
            [
                "03_mozi_architecture_tree.md",
                "MCP/11_Document/document_standard.md",
                "MCP/TASK_FLOW.md",
            ],
            ["04_yingzheng_document_tree.md", "Phase-1 document checklist"],
        )
    )
    next_index += 1
    memory_failure = [
        item.id
        for item in invocations
        if item.tool_id == "tool.memory.lookup" and item.status != "SUCCESS"
    ]
    knowledge_failures = [
        item.id
        for item in invocations
        if item.tool_id == "tool.knowledge.lookup" and item.status != "SUCCESS"
    ]
    invocations.append(audit_invocation(next_index, missing_files, knowledge_failures + memory_failure))
    return invocations


def provider_assignment_for_agent(
    agent_id: str,
    agent_defaults: dict[str, dict[str, str]],
    default_provider: str,
) -> dict[str, str]:
    assignment = agent_defaults.get(agent_id, {})
    return {
        "provider_id": assignment.get("provider_id", default_provider),
        "model": assignment.get("model", ""),
    }


def build_v25_invocations(
    agents: dict[str, AgentSpec],
    providers: dict[str, ProviderSpec],
    agent_defaults: dict[str, dict[str, str]],
    default_provider: str,
    project_name: str,
    project_code: str,
    project_type: str,
    missing_files: list[str],
    approvals: list[ApprovalRequest],
) -> list[ToolInvocation]:
    invocations = knowledge_lookup_invocations(1)
    next_index = len(invocations) + 1
    invocations.append(memory_lookup_invocation(next_index))
    next_index += 1

    packets = [
        agent_packet_invocation(
            next_index,
            agents["PM-001"],
            f"为 {project_name} 生成 Phase-1 任务树，并根据能力矩阵决定责任角色。",
            [
                "MCP/PROJECT_PACK_TEMPLATE.md",
                "MCP/TASK_CARD_TEMPLATE.md",
                "MCP/20_Expert_Training/capability_matrix.md",
            ],
            ["02_zhuge_task_tree.md", "任务依赖与审计门禁"],
            provider_assignment_for_agent("PM-001", agent_defaults, default_provider),
        ),
        agent_packet_invocation(
            next_index + 1,
            agents["ARC-001"],
            f"为 {project_name} 生成启动阶段架构树，明确模块边界和禁止编码边界。",
            [
                "02_zhuge_task_tree.md",
                "MCP/02_Architecture/architecture_principles.md",
                "MCP/17_Memory_Center/decision_registry.md",
            ],
            ["03_mozi_architecture_tree.md", "Architecture Decision candidates"],
            provider_assignment_for_agent("ARC-001", agent_defaults, default_provider),
        ),
        agent_packet_invocation(
            next_index + 2,
            agents["DOC-001"],
            f"为 {project_name} 生成文档树，保持先文档后开发。",
            [
                "03_mozi_architecture_tree.md",
                "MCP/11_Document/document_standard.md",
                "MCP/TASK_FLOW.md",
            ],
            ["04_yingzheng_document_tree.md", "Phase-1 document checklist"],
            provider_assignment_for_agent("DOC-001", agent_defaults, default_provider),
        ),
    ]
    invocations.extend(packets)
    next_index += len(packets)

    for packet in packets:
        invocations.append(provider_invoke_invocation(next_index, packet, providers))
        next_index += 1

    invocations.extend(approval_invocations(next_index, approvals))
    next_index += len(approvals)

    memory_failure = [
        item.id
        for item in invocations
        if item.tool_id == "tool.memory.lookup" and item.status != "SUCCESS"
    ]
    knowledge_failures = [
        item.id
        for item in invocations
        if item.tool_id == "tool.knowledge.lookup" and item.status != "SUCCESS"
    ]
    provider_failures = [
        item.id
        for item in invocations
        if item.tool_id == "tool.provider.invoke" and item.status == "FAIL"
    ]
    invocations.append(
        audit_invocation_v25(
            next_index,
            missing_files,
            knowledge_failures + memory_failure + provider_failures,
            approvals,
        )
    )
    return invocations


def build_v26_invocations(
    agents: dict[str, AgentSpec],
    providers: dict[str, ProviderSpec],
    agent_defaults: dict[str, dict[str, str]],
    default_provider: str,
    project_name: str,
    project_code: str,
    project_type: str,
    missing_files: list[str],
    approvals: list[ApprovalRequest],
) -> list[ToolInvocation]:
    invocations = knowledge_lookup_invocations(1)
    next_index = len(invocations) + 1
    invocations.append(memory_lookup_invocation(next_index))
    next_index += 1

    packets = [
        agent_packet_invocation(
            next_index,
            agents["PM-001"],
            f"为 {project_name} 生成 Phase-1 任务树，并根据能力矩阵决定责任角色。",
            [
                "MCP/PROJECT_PACK_TEMPLATE.md",
                "MCP/TASK_CARD_TEMPLATE.md",
                "MCP/20_Expert_Training/capability_matrix.md",
            ],
            ["02_zhuge_task_tree.md", "任务依赖与审计门禁"],
            provider_assignment_for_agent("PM-001", agent_defaults, default_provider),
        ),
        agent_packet_invocation(
            next_index + 1,
            agents["ARC-001"],
            f"为 {project_name} 生成启动阶段架构树，明确模块边界和禁止编码边界。",
            [
                "02_zhuge_task_tree.md",
                "MCP/02_Architecture/architecture_principles.md",
                "MCP/17_Memory_Center/decision_registry.md",
            ],
            ["03_mozi_architecture_tree.md", "Architecture Decision candidates"],
            provider_assignment_for_agent("ARC-001", agent_defaults, default_provider),
        ),
        agent_packet_invocation(
            next_index + 2,
            agents["DOC-001"],
            f"为 {project_name} 生成文档树，保持先文档后开发。",
            [
                "03_mozi_architecture_tree.md",
                "MCP/11_Document/document_standard.md",
                "MCP/TASK_FLOW.md",
            ],
            ["04_yingzheng_document_tree.md", "Phase-1 document checklist"],
            provider_assignment_for_agent("DOC-001", agent_defaults, default_provider),
        ),
    ]
    invocations.extend(packets)
    next_index += len(packets)

    for packet in packets:
        invocations.append(provider_execute_invocation(next_index, packet, providers))
        next_index += 1

    invocations.extend(approval_invocations(next_index, approvals))
    next_index += len(approvals)

    memory_failure = [
        item.id
        for item in invocations
        if item.tool_id == "tool.memory.lookup" and item.status != "SUCCESS"
    ]
    knowledge_failures = [
        item.id
        for item in invocations
        if item.tool_id == "tool.knowledge.lookup" and item.status != "SUCCESS"
    ]
    provider_failures = [
        item.id
        for item in invocations
        if item.tool_id == "tool.provider.invoke" and item.status == "FAIL"
    ]
    invocations.append(
        audit_invocation_v25(
            next_index,
            missing_files,
            knowledge_failures + memory_failure + provider_failures,
            approvals,
        )
    )
    return invocations


def start_project_v2(project_name: str, project_code: str, project_type: str, output_dir: str | None) -> Path:
    agents = load_agents()
    tools = build_tool_registry()
    missing_files = check_required_files()
    safe_code = safe_project_code(project_code)
    run_id = f"{safe_code}_v2_{timestamp()}"
    out_dir = Path(output_dir) if output_dir else RUNTIME_ROOT / "tasks" / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    invocations = build_v2_invocations(agents, project_name, safe_code, project_type, missing_files)
    tool_failures = [
        item.id
        for item in invocations
        if item.status == "FAIL"
    ]
    audit_status = "AUDIT_PASS" if not missing_files and not tool_failures else "AUDIT_FAIL"

    context = build_runtime_context("OMCF_Runtime_V2", project_name, project_code, project_type, agents, tools)
    context["run_id"] = run_id
    context["status"] = audit_status
    context["tool_invocation_count"] = len(invocations)
    context["external_agent_calls"] = [
        item.id for item in invocations if item.status == "READY_FOR_EXTERNAL_AGENT"
    ]

    write_json(out_dir / "00_runtime_context.json", context)
    write_json(out_dir / "00_tool_registry.json", tool_summary(tools))
    write_text(out_dir / "01_nuwa_project_bootstrap.md", render_nuwa(project_name, project_code, project_type, agents["CAIO-001"], "OMCF_Runtime_V2"))
    write_text(out_dir / "02_zhuge_task_tree.md", render_task_tree(project_name, safe_code, agents["PM-001"]))
    write_text(out_dir / "03_mozi_architecture_tree.md", render_architecture_tree(project_name, project_type, agents["ARC-001"]))
    write_text(out_dir / "04_yingzheng_document_tree.md", render_document_tree(project_name, agents["DOC-001"]))
    write_text(out_dir / "05_tool_layer_report.md", render_tool_layer_report(tools, invocations))
    write_text(out_dir / "06_agent_call_packets.md", render_agent_call_packets(invocations))
    write_jsonl(out_dir / "07_tool_invocations.jsonl", invocation_dicts(invocations))
    write_text(out_dir / "08_zhaoyun_audit_report.md", render_audit_report(project_name, missing_files, agents["AUD-001"], tool_failures))

    return out_dir


def start_project_v25(
    project_name: str,
    project_code: str,
    project_type: str,
    output_dir: str | None,
    sensitive_scopes: list[str],
) -> Path:
    agents = load_agents()
    tools = build_tool_registry()
    providers, agent_defaults, default_provider = load_provider_registry()
    missing_files = check_required_files()
    approvals = approval_requests_for_scopes(sensitive_scopes)
    safe_code = safe_project_code(project_code)
    run_id = f"{safe_code}_v2_5_{timestamp()}"
    out_dir = Path(output_dir) if output_dir else RUNTIME_ROOT / "tasks" / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    invocations = build_v25_invocations(
        agents,
        providers,
        agent_defaults,
        default_provider,
        project_name,
        safe_code,
        project_type,
        missing_files,
        approvals,
    )
    tool_failures = [
        item.id
        for item in invocations
        if item.status == "FAIL"
    ]
    if missing_files or tool_failures:
        audit_status = "AUDIT_FAIL"
    elif approvals:
        audit_status = "WAIT_HUMAN_APPROVAL"
    else:
        audit_status = "AUDIT_PASS"

    context = build_runtime_context("OMCF_Runtime_V2_5", project_name, project_code, project_type, agents, tools, providers)
    context["run_id"] = run_id
    context["status"] = audit_status
    context["tool_invocation_count"] = len(invocations)
    context["provider_invocation_count"] = len([item for item in invocations if item.tool_id == "tool.provider.invoke"])
    context["approval_count"] = len(approvals)
    context["external_agent_calls"] = [
        item.id for item in invocations if item.status == "READY_FOR_EXTERNAL_AGENT"
    ]
    context["provider_routes"] = [
        item.id for item in invocations if item.tool_id == "tool.provider.invoke"
    ]
    context["approval_requests"] = [item.id for item in approvals]

    write_json(out_dir / "00_runtime_context.json", context)
    write_json(out_dir / "00_tool_registry.json", tool_summary(tools))
    write_json(out_dir / "00_provider_registry.json", provider_summary(providers))
    write_text(out_dir / "01_nuwa_project_bootstrap.md", render_nuwa(project_name, project_code, project_type, agents["CAIO-001"], "OMCF_Runtime_V2_5"))
    write_text(out_dir / "02_zhuge_task_tree.md", render_task_tree(project_name, safe_code, agents["PM-001"]))
    write_text(out_dir / "03_mozi_architecture_tree.md", render_architecture_tree(project_name, project_type, agents["ARC-001"]))
    write_text(out_dir / "04_yingzheng_document_tree.md", render_document_tree(project_name, agents["DOC-001"]))
    write_text(out_dir / "05_tool_layer_report.md", render_tool_layer_report(tools, invocations))
    write_text(out_dir / "06_provider_execution_plan.md", render_provider_execution_plan(providers, invocations))
    write_text(out_dir / "07_agent_call_packets.md", render_agent_call_packets(invocations))
    write_jsonl(out_dir / "08_tool_invocations.jsonl", invocation_dicts(invocations))
    write_json(out_dir / "09_human_approval_requests.json", {"approval_requests": approval_dicts(approvals)})
    write_text(out_dir / "09_human_approval_report.md", render_human_approval_report(approvals))
    write_text(out_dir / "10_zhaoyun_audit_report.md", render_audit_report(project_name, missing_files, agents["AUD-001"], tool_failures, approvals))

    return out_dir


def start_project_v26(
    project_name: str,
    project_code: str,
    project_type: str,
    output_dir: str | None,
    sensitive_scopes: list[str],
) -> Path:
    agents = load_agents()
    tools = build_tool_registry()
    providers, agent_defaults, default_provider = load_provider_registry()
    missing_files = check_required_files()
    approvals = approval_requests_for_scopes(sensitive_scopes)
    safe_code = safe_project_code(project_code)
    run_id = f"{safe_code}_v2_6_{timestamp()}"
    out_dir = Path(output_dir) if output_dir else RUNTIME_ROOT / "tasks" / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    invocations = build_v26_invocations(
        agents,
        providers,
        agent_defaults,
        default_provider,
        project_name,
        safe_code,
        project_type,
        missing_files,
        approvals,
    )
    tool_failures = [
        item.id
        for item in invocations
        if item.status == "FAIL"
    ]
    if missing_files or tool_failures:
        audit_status = "AUDIT_FAIL"
    elif approvals:
        audit_status = "WAIT_HUMAN_APPROVAL"
    else:
        audit_status = "AUDIT_PASS"

    queue_entries = write_human_queue_items(run_id, project_name, approvals)
    metrics_report = build_metrics_report("OMCF_Runtime_V2_6", run_id, project_name, invocations, approvals, audit_status)
    persistent_metric_paths = update_persistent_metrics(metrics_report)

    context = build_runtime_context("OMCF_Runtime_V2_6", project_name, project_code, project_type, agents, tools, providers)
    context["run_id"] = run_id
    context["status"] = audit_status
    context["tool_invocation_count"] = len(invocations)
    context["provider_invocation_count"] = len([item for item in invocations if item.tool_id == "tool.provider.invoke"])
    context["provider_executed_count"] = len([item for item in invocations if item.status == "PROVIDER_EXECUTED"])
    context["approval_count"] = len(approvals)
    context["human_queue_entries"] = [item["queue_path"] for item in queue_entries]
    context["metrics_files"] = persistent_metric_paths
    context["external_agent_calls"] = [
        item.id for item in invocations if item.status == "READY_FOR_EXTERNAL_AGENT"
    ]
    context["provider_adapter_results"] = [
        item.id for item in invocations if item.tool_id == "tool.provider.invoke"
    ]
    context["approval_requests"] = [item.id for item in approvals]

    write_json(out_dir / "00_runtime_context.json", context)
    write_json(out_dir / "00_tool_registry.json", tool_summary(tools))
    write_json(out_dir / "00_provider_registry.json", provider_summary(providers))
    write_text(out_dir / "01_nuwa_project_bootstrap.md", render_nuwa(project_name, project_code, project_type, agents["CAIO-001"], "OMCF_Runtime_V2_6"))
    write_text(out_dir / "02_zhuge_task_tree.md", render_task_tree(project_name, safe_code, agents["PM-001"]))
    write_text(out_dir / "03_mozi_architecture_tree.md", render_architecture_tree(project_name, project_type, agents["ARC-001"]))
    write_text(out_dir / "04_yingzheng_document_tree.md", render_document_tree(project_name, agents["DOC-001"]))
    write_text(out_dir / "05_tool_layer_report.md", render_tool_layer_report(tools, invocations))
    write_text(out_dir / "06_provider_execution_plan.md", render_provider_execution_plan(providers, invocations))
    write_text(out_dir / "07_provider_adapter_results.md", render_provider_adapter_results(invocations))
    write_text(out_dir / "08_agent_call_packets.md", render_agent_call_packets(invocations))
    write_jsonl(out_dir / "09_tool_invocations.jsonl", invocation_dicts(invocations))
    write_json(out_dir / "10_human_approval_requests.json", {"approval_requests": approval_dicts(approvals)})
    write_json(out_dir / "11_human_queue_entries.json", {"human_queue_entries": queue_entries})
    write_text(out_dir / "11_human_approval_report.md", render_human_approval_report(approvals))
    write_json(out_dir / "12_metrics_report.json", metrics_report)
    write_text(out_dir / "12_metrics_report.md", render_metrics_report(metrics_report, persistent_metric_paths))
    write_text(out_dir / "13_zhaoyun_audit_report.md", render_audit_report(project_name, missing_files, agents["AUD-001"], tool_failures, approvals))

    return out_dir


def list_tools() -> None:
    print(json.dumps(tool_summary(build_tool_registry()), ensure_ascii=False, indent=2))


def list_providers() -> None:
    providers, agent_defaults, default_provider = load_provider_registry()
    payload = {
        "default_provider": default_provider,
        "providers": provider_summary(providers),
        "agent_defaults": agent_defaults,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def list_human_queue() -> None:
    print(json.dumps({"human_queue": list_local_json_files(HUMAN_QUEUE_DIR)}, ensure_ascii=False, indent=2))


def list_metrics() -> None:
    print(json.dumps({"metrics": list_local_json_files(METRICS_DIR)}, ensure_ascii=False, indent=2))


def invoke_codex_provider(task_file: str, output_dir: str, sandbox: str, timeout_seconds: int) -> int:
    adapter = PROVIDERS_ROOT / "codex" / "codex_adapter.py"
    command = [
        sys.executable,
        str(adapter),
        "--task-file",
        task_file,
        "--output-dir",
        output_dir,
        "--sandbox",
        sandbox,
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="OMCF Runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start-project", help="Start a Runtime V1 project bootstrap chain")
    start.add_argument("--project-name", required=True)
    start.add_argument("--project-code", required=True)
    start.add_argument("--project-type", required=True)
    start.add_argument("--output-dir", default=None)

    start_v2 = subparsers.add_parser("start-project-v2", help="Start a Runtime V2 project bootstrap chain with Tool Layer records")
    start_v2.add_argument("--project-name", required=True)
    start_v2.add_argument("--project-code", required=True)
    start_v2.add_argument("--project-type", required=True)
    start_v2.add_argument("--output-dir", default=None)

    start_v25 = subparsers.add_parser("start-project-v2-5", help="Start a Runtime V2.5 chain with Provider Layer and human approval gates")
    start_v25.add_argument("--project-name", required=True)
    start_v25.add_argument("--project-code", required=True)
    start_v25.add_argument("--project-type", required=True)
    start_v25.add_argument("--output-dir", default=None)
    start_v25.add_argument(
        "--sensitive-scope",
        action="append",
        default=[],
        help="Protected scope requiring human approval, such as database_schema, bank_interface, ai_training_data, production_deploy, or aoem_core_logic",
    )

    start_v26 = subparsers.add_parser("start-project-v2-6", help="Start a Runtime V2.6 chain with provider adapters, human queue, and metrics")
    start_v26.add_argument("--project-name", required=True)
    start_v26.add_argument("--project-code", required=True)
    start_v26.add_argument("--project-type", required=True)
    start_v26.add_argument("--output-dir", default=None)
    start_v26.add_argument(
        "--sensitive-scope",
        action="append",
        default=[],
        help="Protected scope requiring human approval, such as database_schema, bank_interface, ai_training_data, production_deploy, or aoem_core_logic",
    )

    subparsers.add_parser("list-tools", help="Print the Runtime V2 tool registry")
    subparsers.add_parser("list-providers", help="Print the Runtime V2.5 provider registry")
    subparsers.add_parser("list-human-queue", help="Print local Runtime V2.6 human approval queue")
    subparsers.add_parser("list-metrics", help="Print local Runtime V2.6 metrics")

    invoke_codex = subparsers.add_parser("invoke-codex", help="Invoke the real local Codex CLI provider adapter")
    invoke_codex.add_argument("--task-file", required=True)
    invoke_codex.add_argument("--output-dir", required=True)
    invoke_codex.add_argument("--sandbox", default="read-only", choices=["read-only", "workspace-write", "danger-full-access"])
    invoke_codex.add_argument("--timeout-seconds", type=int, default=600)

    args = parser.parse_args()

    if args.command == "start-project":
        out_dir = start_project(args.project_name, args.project_code, args.project_type, args.output_dir)
        print(f"OMCF Runtime V1 completed: {out_dir}")
        return 0

    if args.command == "start-project-v2":
        out_dir = start_project_v2(args.project_name, args.project_code, args.project_type, args.output_dir)
        print(f"OMCF Runtime V2 completed: {out_dir}")
        return 0

    if args.command == "start-project-v2-5":
        out_dir = start_project_v25(
            args.project_name,
            args.project_code,
            args.project_type,
            args.output_dir,
            args.sensitive_scope,
        )
        print(f"OMCF Runtime V2.5 completed: {out_dir}")
        return 0

    if args.command == "start-project-v2-6":
        out_dir = start_project_v26(
            args.project_name,
            args.project_code,
            args.project_type,
            args.output_dir,
            args.sensitive_scope,
        )
        print(f"OMCF Runtime V2.6 completed: {out_dir}")
        return 0

    if args.command == "list-tools":
        list_tools()
        return 0

    if args.command == "list-providers":
        list_providers()
        return 0

    if args.command == "list-human-queue":
        list_human_queue()
        return 0

    if args.command == "list-metrics":
        list_metrics()
        return 0

    if args.command == "invoke-codex":
        return invoke_codex_provider(
            task_file=args.task_file,
            output_dir=args.output_dir,
            sandbox=args.sandbox,
            timeout_seconds=args.timeout_seconds,
        )

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
