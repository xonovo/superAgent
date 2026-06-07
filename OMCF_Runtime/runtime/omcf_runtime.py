from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "OMCF_Runtime"
MCP_ROOT = REPO_ROOT / "MCP"


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


def build_runtime_context(
    runtime_version: str,
    project_name: str,
    project_code: str,
    project_type: str,
    agents: dict[str, AgentSpec],
    tools: dict[str, ToolSpec] | None = None,
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
    return new_invocation(
        index,
        "CAIO-001",
        "tool.memory.lookup",
        "check_project_memory_template",
        "SUCCESS" if template.exists() and not project_slots else "FAIL",
        {"template": rel_path(template)},
        {
            "template_exists": template.exists(),
            "project_slots": project_slots,
            "policy": "Project_Memory keeps template only until a real project is explicitly started.",
        },
    )


def agent_packet_invocation(
    index: int,
    agent: AgentSpec,
    objective: str,
    required_inputs: list[str],
    expected_outputs: list[str],
) -> ToolInvocation:
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
            "adapter": "codex_or_gpt",
            "execution_note": "Runtime V2 records the call contract. A Codex/GPT adapter can execute it later.",
        },
    )


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


def render_audit_report(project_name: str, missing_files: list[str], agent: AgentSpec, tool_failures: list[str] | None = None) -> str:
    failures = tool_failures or []
    status = "PASS" if not missing_files and not failures else "FAIL"
    missing_text = "\n".join(f"- {item}" for item in missing_files) if missing_files else "- 无"
    failure_text = "\n".join(f"- {item}" for item in failures) if failures else "- 无"
    opinion = "启动链路可进入下一步任务规划。" if status == "PASS" else "存在关键缺口，不得进入下一步。"
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


def list_tools() -> None:
    print(json.dumps(tool_summary(build_tool_registry()), ensure_ascii=False, indent=2))


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

    subparsers.add_parser("list-tools", help="Print the Runtime V2 tool registry")

    args = parser.parse_args()

    if args.command == "start-project":
        out_dir = start_project(args.project_name, args.project_code, args.project_type, args.output_dir)
        print(f"OMCF Runtime V1 completed: {out_dir}")
        return 0

    if args.command == "start-project-v2":
        out_dir = start_project_v2(args.project_name, args.project_code, args.project_type, args.output_dir)
        print(f"OMCF Runtime V2 completed: {out_dir}")
        return 0

    if args.command == "list-tools":
        list_tools()
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
