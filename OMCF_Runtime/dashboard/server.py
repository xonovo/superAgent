from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BASE_DIR.parent
REPO_ROOT = RUNTIME_DIR.parent
STATIC_DIR = BASE_DIR / "static"
STATE_DIR = BASE_DIR / "state"

AGENTS_DIR = RUNTIME_DIR / "agents"
PROVIDERS_FILE = RUNTIME_DIR / "providers" / "providers.json"
METRICS_DIR = RUNTIME_DIR / "runtime" / "metrics"
HUMAN_QUEUE_DIR = RUNTIME_DIR / "audit" / "human_queue"
PROJECT_MEMORY_DIR = (
    REPO_ROOT
    / "MCP"
    / "17_Memory_Center"
    / "Project_Memory"
    / "Zhuzhou_Property_Platform"
)
DECISION_LOG = STATE_DIR / "human_queue_decisions.jsonl"
RUN_REQUEST_LOG = STATE_DIR / "run_requests.jsonl"
SAFE_EXECUTION_EVENT_LOG = STATE_DIR / "safe_execution_events.jsonl"
SAFE_EXECUTION_QUEUE_LOG = STATE_DIR / "safe_execution_queue.jsonl"
PRODUCTION_ALLOWLIST_FILE = STATE_DIR / "production_allowlist.json"

TASK_TYPE_POLICIES: dict[str, dict[str, Any]] = {
    "document": {
        "risk": "low",
        "required_gates": ["dry_run"],
        "execution_mode": "safe_queue_document",
    },
    "code": {
        "risk": "medium",
        "required_gates": ["dry_run", "audit_pass"],
        "execution_mode": "safe_queue_codex_read_only",
    },
    "restricted": {
        "risk": "high",
        "required_gates": ["dry_run", "human_approval", "audit_pass"],
        "execution_mode": "safe_queue_requires_operator",
    },
    "production": {
        "risk": "critical",
        "required_gates": ["dry_run", "production_whitelist", "human_approval", "audit_pass"],
        "execution_mode": "blocked_by_default",
    },
}

GATE_LABELS = {
    "dry_run": "Dry Run",
    "human_approval": "King Xu Approval",
    "audit_pass": "Zhao Yun Audit",
    "production_whitelist": "Production Whitelist",
}


ROLE_CATALOG: list[dict[str, Any]] = [
    {
        "id": "KING-XU",
        "nickname": "King Xu",
        "name": "KingXu",
        "role": "Human Decision Maker",
        "department": "board",
        "parent": None,
        "avatar": "KX",
        "accent": "#7c3aed",
    },
    {
        "id": "CAIO-001",
        "nickname": "女娲",
        "name": "Nuwa",
        "role": "Chief AI Officer",
        "department": "executive",
        "parent": "KING-XU",
        "avatar": "女",
        "accent": "#0f766e",
    },
    {
        "id": "PM-001",
        "nickname": "诸葛亮",
        "name": "ZhugeLiang",
        "role": "CEO / Project Manager",
        "department": "executive",
        "parent": "CAIO-001",
        "avatar": "诸",
        "accent": "#2563eb",
    },
    {
        "id": "ARC-001",
        "nickname": "墨子",
        "name": "Mozi",
        "role": "CTO / Chief Architect",
        "department": "executive",
        "parent": "CAIO-001",
        "avatar": "墨",
        "accent": "#0f766e",
    },
    {
        "id": "DOC-001",
        "nickname": "嬴政",
        "name": "YingZheng",
        "role": "CAO / Document Officer",
        "department": "executive",
        "parent": "CAIO-001",
        "avatar": "嬴",
        "accent": "#9333ea",
    },
    {
        "id": "AUD-001",
        "nickname": "赵云",
        "name": "ZhaoYun",
        "role": "Chief Auditor",
        "department": "audit",
        "parent": "CAIO-001",
        "avatar": "赵",
        "accent": "#dc2626",
    },
    {
        "id": "DB-001",
        "nickname": "鲁班七号",
        "name": "LubanQihao",
        "role": "Database Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "鲁",
        "accent": "#0891b2",
    },
    {
        "id": "DATA-001",
        "nickname": "项羽",
        "name": "XiangYu",
        "role": "Data Governance Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "项",
        "accent": "#ca8a04",
    },
    {
        "id": "BE-001",
        "nickname": "司马懿",
        "name": "SimaYi",
        "role": "Backend Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "司",
        "accent": "#475569",
    },
    {
        "id": "FE-001",
        "nickname": "妲己",
        "name": "Daji",
        "role": "Frontend Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "妲",
        "accent": "#db2777",
    },
    {
        "id": "MOB-001",
        "nickname": "孙尚香",
        "name": "SunShangXiang",
        "role": "Mobile Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "孙",
        "accent": "#ea580c",
    },
    {
        "id": "UI-001",
        "nickname": "貂蝉",
        "name": "DiaoChan",
        "role": "Design Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "貂",
        "accent": "#be185d",
    },
    {
        "id": "API-001",
        "nickname": "刘备",
        "name": "LiuBei",
        "role": "Interface Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "刘",
        "accent": "#16a34a",
    },
    {
        "id": "OPS-001",
        "nickname": "张飞",
        "name": "ZhangFei",
        "role": "Infrastructure Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "张",
        "accent": "#334155",
    },
    {
        "id": "AI-001",
        "nickname": "王昭君",
        "name": "WangZhaojun",
        "role": "AI R&D Director",
        "department": "engineering",
        "parent": "ARC-001",
        "avatar": "王",
        "accent": "#0284c7",
    },
    {
        "id": "AOEM-001",
        "nickname": "庞统",
        "name": "PangTong",
        "role": "AOEM Expert",
        "department": "expert",
        "parent": "ARC-001",
        "avatar": "庞",
        "accent": "#7c2d12",
    },
    {
        "id": "MATH-001",
        "nickname": "华佗",
        "name": "HuaTuo",
        "role": "Math Expert",
        "department": "expert",
        "parent": "ARC-001",
        "avatar": "华",
        "accent": "#4d7c0f",
    },
    {
        "id": "LANG-001",
        "nickname": "庄周",
        "name": "ZhuangZhou",
        "role": "Language Evolution Expert",
        "department": "expert",
        "parent": "ARC-001",
        "avatar": "庄",
        "accent": "#0369a1",
    },
    {
        "id": "KNOW-001",
        "nickname": "伏羲",
        "name": "FuXi",
        "role": "Chief Knowledge Officer",
        "department": "knowledge",
        "parent": "CAIO-001",
        "avatar": "伏",
        "accent": "#059669",
    },
    {
        "id": "STR-001",
        "nickname": "鬼谷子",
        "name": "GuiGuZi",
        "role": "Chief Strategy Officer",
        "department": "knowledge",
        "parent": "CAIO-001",
        "avatar": "鬼",
        "accent": "#a16207",
    },
    {
        "id": "LEARN-001",
        "nickname": "扁鹊",
        "name": "BianQue",
        "role": "Chief Learning Officer",
        "department": "knowledge",
        "parent": "CAIO-001",
        "avatar": "扁",
        "accent": "#0d9488",
    },
    {
        "id": "MEM-001",
        "nickname": "仓颉",
        "name": "CangJie",
        "role": "Chief Memory Officer",
        "department": "knowledge",
        "parent": "CAIO-001",
        "avatar": "仓",
        "accent": "#4338ca",
    },
]


STATUS_LABELS = {
    "running": "Running",
    "waiting": "Waiting",
    "audit": "Audit",
    "human": "Human Approval",
    "idle": "Idle",
    "complete": "Complete",
    "blocked": "Blocked",
}


class QueueDecision(BaseModel):
    decision: str
    note: str | None = None


class StartRunRequest(BaseModel):
    project: str | None = None
    task_id: str | None = None
    agent_id: str | None = None
    title: str | None = None
    note: str | None = None


class CommandEventRequest(BaseModel):
    note: str | None = None


class WorkerRunRequest(BaseModel):
    command_id: str | None = None
    dry_run: bool = True
    limit: int = 1
    timeout_seconds: int = 300


app = FastAPI(title="OMCF Dashboard Alpha", version="alpha")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"status": "PARSE_ERROR", "raw": line, "source": str(path)})
    return rows


def parse_agent_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[4:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = value
                current_list_key = None
            else:
                data[key] = []
                current_list_key = key
    return data


def load_agent_profiles() -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    if not AGENTS_DIR.exists():
        return profiles
    for path in AGENTS_DIR.glob("*.yaml"):
        profile = parse_agent_yaml(path)
        agent_id = profile.get("id")
        if agent_id:
            profile["profile_path"] = str(path.relative_to(REPO_ROOT))
            profiles[agent_id] = profile
    return profiles


def load_metrics() -> dict[str, dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}
    if not METRICS_DIR.exists():
        return metrics
    for path in sorted(METRICS_DIR.glob("*.json")):
        data = read_json(path, {})
        agent_id = data.get("agent_id") or path.stem
        data["source"] = str(path.relative_to(REPO_ROOT))
        metrics[agent_id] = data
    return metrics


def load_human_queue() -> list[dict[str, Any]]:
    decisions = load_queue_decisions()
    entries: list[dict[str, Any]] = []
    if not HUMAN_QUEUE_DIR.exists():
        return entries
    for path in sorted(HUMAN_QUEUE_DIR.glob("*.json")):
        data = read_json(path, {})
        if not data:
            continue
        item_key = queue_item_key(data)
        last_decision = decisions.get(item_key)
        data["item_key"] = item_key
        data["source"] = str(path.relative_to(REPO_ROOT))
        data["dashboard_decision"] = last_decision
        data["dashboard_alpha_only"] = True
        entries.append(data)
    return entries


def queue_item_key(item: dict[str, Any]) -> str:
    run_id = item.get("run_id", "unknown_run")
    queue_id = item.get("queue_id", "unknown_queue")
    return f"{run_id}::{queue_id}"


def load_queue_decisions() -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(DECISION_LOG):
        item_key = row.get("item_key")
        if item_key:
            decisions[item_key] = row
    return decisions


def load_run_requests(tasks: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows = read_jsonl(RUN_REQUEST_LOG)
    events = load_safe_execution_events()
    return [
        enrich_command(row, events.get(row["command_id"], []), tasks or [])
        for row in rows
        if row.get("command_id")
    ]


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_safe_execution_events() -> dict[str, list[dict[str, Any]]]:
    events: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(SAFE_EXECUTION_EVENT_LOG):
        command_id = row.get("command_id")
        if command_id:
            events.setdefault(command_id, []).append(row)
    return events


def load_production_allowlist() -> set[str]:
    payload = read_json(PRODUCTION_ALLOWLIST_FILE, {})
    if isinstance(payload, dict):
        return set(payload.get("command_ids", []))
    if isinstance(payload, list):
        return set(payload)
    return set()


def classify_task(task: dict[str, Any] | None, command: dict[str, Any]) -> dict[str, Any]:
    title = str(command.get("task_title") or (task or {}).get("title") or "")
    note = str(command.get("note") or "")
    phase = str((task or {}).get("phase") or "")
    artifact = str((task or {}).get("artifact") or "")
    agent_id = str(command.get("agent_id") or (task or {}).get("assignee") or "")
    text = " ".join([title, note, phase, artifact, agent_id]).lower()

    production_keywords = ["生产", "production", "prod", "上线", "release"]
    restricted_keywords = [
        "数据库",
        "database",
        "schema",
        "ddl",
        "银行",
        "bank",
        "支付",
        "payment",
        "aoem",
        "部署",
        "deploy",
        "docker",
        "k8s",
        "gpu",
        "隐私计算",
        "privacy",
    ]
    code_keywords = [
        "代码",
        "code",
        "backend",
        "frontend",
        "mobile",
        "sdk",
        "api",
        "实现",
        "开发",
        "编译",
    ]

    if any(keyword in text for keyword in production_keywords):
        task_type = "production"
    elif agent_id in {"DB-001", "API-001", "OPS-001", "AOEM-001"} or any(
        keyword in text for keyword in restricted_keywords
    ):
        task_type = "restricted"
    elif agent_id in {"BE-001", "FE-001", "MOB-001"} or any(keyword in text for keyword in code_keywords):
        task_type = "code"
    else:
        task_type = "document"

    policy = TASK_TYPE_POLICIES[task_type]
    return {
        "task_type": task_type,
        "risk": policy["risk"],
        "required_gates": policy["required_gates"],
        "execution_mode": policy["execution_mode"],
        "production_default_denied": task_type == "production",
        "matched_text": title,
    }


def gate_passed(gate_id: str, events: list[dict[str, Any]], classification: dict[str, Any]) -> bool:
    if gate_id == "dry_run":
        return True
    if gate_id == "human_approval":
        return any(event.get("type") == "HUMAN_APPROVAL_GRANTED" for event in events)
    if gate_id == "audit_pass":
        return any(event.get("type") == "AUDIT_PASSED" for event in events)
    if gate_id == "production_whitelist":
        return any(event.get("type") == "PRODUCTION_WHITELIST_GRANTED" for event in events)
    return False


def command_task_lookup(tasks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {task["id"]: task for task in tasks if task.get("id")}


def enrich_command(
    command: dict[str, Any],
    events: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
) -> dict[str, Any]:
    task = command_task_lookup(tasks).get(command.get("task_id", ""))
    classification = classify_task(task, command)
    allowlisted_ids = load_production_allowlist()
    if command.get("command_id") in allowlisted_ids:
        events = [
            *events,
            {
                "type": "PRODUCTION_WHITELIST_GRANTED",
                "source": "production_allowlist.json",
                "recorded_at": datetime.now().isoformat(timespec="seconds"),
            },
        ]

    dry_run = {
        "status": "PASS",
        "task_type": classification["task_type"],
        "risk": classification["risk"],
        "execution_mode": classification["execution_mode"],
        "production_default_denied": classification["production_default_denied"],
        "sandbox": "read-only",
        "checks": [
            "Classify task risk",
            "Resolve required gates",
            "Block production by default",
            "Keep execution inside Dashboard state queue",
        ],
    }
    required_gates = classification["required_gates"]
    gates = []
    missing = []
    for gate_id in required_gates:
        passed = gate_passed(gate_id, events, classification)
        if not passed:
            missing.append(gate_id)
        gates.append(
            {
                "id": gate_id,
                "label": GATE_LABELS[gate_id],
                "required": True,
                "status": "PASS" if passed else "WAITING",
            }
        )

    rejected = any(event.get("type") in {"HUMAN_REJECTED", "AUDIT_REJECTED"} for event in events)
    queued = any(event.get("type") == "SAFE_EXECUTION_QUEUED" for event in events)
    worker_completed = any(event.get("type") == "WORKER_COMPLETED" for event in events)
    worker_failed = any(event.get("type") == "WORKER_FAILED" for event in events)
    worker_rejected = any(event.get("type") == "WORKER_REJECTED" for event in events)
    if rejected:
        status = "REJECTED"
    elif worker_completed:
        status = "WORKER_COMPLETED"
    elif worker_failed:
        status = "WORKER_FAILED"
    elif worker_rejected:
        status = "WORKER_REJECTED"
    elif queued:
        status = "SAFE_EXECUTION_QUEUED"
    elif "production_whitelist" in missing:
        status = "BLOCKED_PRODUCTION_DEFAULT_DENY"
    elif "human_approval" in missing:
        status = "WAIT_HUMAN_APPROVAL"
    elif "audit_pass" in missing:
        status = "WAIT_AUDIT_PASS"
    elif missing:
        status = "WAIT_GATE"
    else:
        status = "READY_FOR_SAFE_EXECUTION"

    enriched = dict(command)
    enriched.update(
        {
            "status": status,
            "dry_run": dry_run,
            "gates": gates,
            "missing_gates": missing,
            "events": events,
            "safe_execution": {
                "can_execute": status == "READY_FOR_SAFE_EXECUTION",
                "can_worker_run": status == "SAFE_EXECUTION_QUEUED",
                "queue_status": "queued" if queued else "not_queued",
                "production_default_denied": classification["production_default_denied"],
            },
        }
    )
    return enriched


def build_safe_execution_packet(command: dict[str, Any]) -> dict[str, Any]:
    command_id = command["command_id"]
    output_dir = STATE_DIR / "safe_execution" / command_id
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / "task_packet.json"
    packet = {
        "task_id": command.get("task_id"),
        "command_id": command_id,
        "project": command.get("project"),
        "agent_id": command.get("agent_id"),
        "agent": command.get("agent"),
        "task_title": command.get("task_title"),
        "provider_id": "provider.codex",
        "sandbox": "read-only",
        "execution_mode": command.get("dry_run", {}).get("execution_mode"),
        "prompt": (
            "Execute this OMCF task only within the documented safe boundary. "
            "Do not change databases, bank interfaces, AOEM runtime, deployment, or production systems. "
            f"Task: {command.get('task_title')}"
        ),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dashboard_alpha_only": True,
    }
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "packet": packet,
        "packet_path": display_path(packet_path),
    }


def load_provider_invocations() -> list[dict[str, Any]]:
    candidates = [
        (
            "Production Run 001",
            PROJECT_MEMORY_DIR / "Production_Run_001" / "01_real_provider_invocations.jsonl",
        ),
        (
            "Alpha Run 001",
            PROJECT_MEMORY_DIR / "Alpha_Run_001" / "01_alpha_provider_invocations.jsonl",
        ),
    ]
    invocations: list[dict[str, Any]] = []
    for run_name, path in candidates:
        for index, row in enumerate(read_jsonl(path), start=1):
            row.setdefault("id", f"{run_name}-{index}")
            row["run_name"] = run_name
            row["source"] = str(path.relative_to(REPO_ROOT))
            row["sequence"] = len(invocations) + 1
            invocations.append(row)

    codex_result_path = PROJECT_MEMORY_DIR / "Alpha_Run_002" / "codex_adapter_result.json"
    codex_result = read_json(codex_result_path, {})
    if codex_result:
        invocations.append(
            {
                "id": codex_result.get("task_id", "OMCF-ALPHA-002-CODEX-001"),
                "run_name": "Alpha Run 002",
                "provider_id": codex_result.get("provider_id", "provider.codex"),
                "provider_channel": "codex_cli_exec",
                "agent_id": codex_result.get("agent_id", "PM-001"),
                "agent": "诸葛亮",
                "task": "Runtime 调用真实 Codex CLI 生成 Project Pack Intake",
                "status": codex_result.get("status", "UNKNOWN"),
                "artifact": codex_result.get("last_message_path"),
                "mock": codex_result.get("mock", False),
                "simulated": codex_result.get("simulated", False),
                "codex_version": codex_result.get("codex_version"),
                "started_at": codex_result.get("started_at"),
                "finished_at": codex_result.get("finished_at"),
                "source": str(codex_result_path.relative_to(REPO_ROOT)),
                "sequence": len(invocations) + 1,
            }
        )
    return invocations


def load_providers(invocations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    registry = read_json(PROVIDERS_FILE, {})
    providers = {item["id"]: dict(item) for item in registry.get("providers", []) if item.get("id")}
    for invocation in invocations:
        provider_id = invocation.get("provider_id", "unknown")
        providers.setdefault(
            provider_id,
            {
                "id": provider_id,
                "name": provider_id,
                "kind": "observed_provider",
                "execution_mode": invocation.get("provider_channel", "observed"),
                "enabled": True,
                "status": "observed",
                "capabilities": [],
            },
        )
        provider = providers[provider_id]
        provider["last_status"] = invocation.get("status")
        provider["last_agent_id"] = invocation.get("agent_id")
        provider["last_task"] = invocation.get("task")
        provider["last_run_name"] = invocation.get("run_name")
        provider["last_artifact"] = invocation.get("artifact")
    return list(providers.values())


def build_agents(
    profiles: dict[str, dict[str, Any]],
    metrics: dict[str, dict[str, Any]],
    queue: list[dict[str, Any]],
    invocations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pending_requesters = {
        item.get("requester")
        for item in queue
        if item.get("queue_status") == "pending" and not item.get("dashboard_decision")
    }
    blocked_agents = {
        item.get("agent_id")
        for item in invocations
        if str(item.get("status", "")).startswith("BLOCKED")
    }
    executed_agents = {
        item.get("agent_id")
        for item in invocations
        if item.get("status") == "PROVIDER_EXECUTED"
    }

    agents: list[dict[str, Any]] = []
    for role in ROLE_CATALOG:
        agent_id = role["id"]
        profile = profiles.get(agent_id, {})
        status = "idle"
        if agent_id in pending_requesters:
            status = "human"
        elif agent_id == "AUD-001" and queue:
            status = "audit"
        elif agent_id in blocked_agents:
            status = "waiting"
        elif agent_id in executed_agents and agent_id in {"CAIO-001", "PM-001", "ARC-001"}:
            status = "running"
        elif agent_id in executed_agents:
            status = "complete"

        merged = {
            **role,
            "role": profile.get("role", role["role"]),
            "responsibility": profile.get("responsibility", ""),
            "capabilities": profile.get("capabilities", []),
            "status": status,
            "status_label": STATUS_LABELS[status],
            "metrics": metrics.get(agent_id, {}),
            "has_runtime_profile": bool(profile),
        }
        agents.append(merged)
    return agents


def artifact_exists(relative_path: str) -> bool:
    return (REPO_ROOT / relative_path).exists()


def build_tasks(commands: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    specs = [
        (
            "PRUN-001",
            "项目启动",
            "CAIO-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/00_run_manifest.md",
        ),
        (
            "PRUN-002",
            "任务树生成",
            "PM-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/02_zhuge_task_tree.md",
        ),
        (
            "PRUN-003",
            "架构树生成",
            "ARC-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/03_mozi_architecture_tree.md",
        ),
        (
            "PRUN-004",
            "PRD V0.1",
            "DOC-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/04_yingzheng_prd.md",
        ),
        (
            "PRUN-005",
            "数据库边界分析",
            "DB-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/05_luban_database_analysis.md",
        ),
        (
            "PRUN-006",
            "数据质量分析",
            "DATA-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/06_xiangyu_data_quality_analysis.md",
        ),
        (
            "PRUN-007",
            "赵云审计",
            "AUD-001",
            "Production Run 001",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/07_zhaoyun_audit_report.md",
        ),
        (
            "ALPHA-002",
            "真实 Codex Adapter",
            "PM-001",
            "Alpha Run 002",
            "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Alpha_Run_002/codex_adapter_result.json",
        ),
    ]
    command_by_task: dict[str, dict[str, Any]] = {}
    for command in commands or []:
        task_id = command.get("task_id")
        if task_id:
            command_by_task[task_id] = command

    tasks = []
    for task_id, title, assignee, phase, artifact in specs:
        exists = artifact_exists(artifact)
        command = command_by_task.get(task_id)
        status = "complete" if exists else "waiting"
        if command and status != "complete":
            status = task_status_from_command(command)
        tasks.append(
            {
                "id": task_id,
                "title": title,
                "assignee": assignee,
                "phase": phase,
                "status": status,
                "artifact": artifact,
                "last_command": command,
            }
        )

    next_tasks = [
            {
                "id": "NEXT-001",
                "title": "Project Pack V1 资料补齐",
                "assignee": "PM-001",
                "phase": "Next Alpha Run",
                "status": "waiting",
                "artifact": "MCP/PROJECT_PACK_TEMPLATE.md",
            },
            {
                "id": "NEXT-002",
                "title": "历史系统与数据库清单",
                "assignee": "DB-001",
                "phase": "Next Alpha Run",
                "status": "human",
                "artifact": "OMCF_Runtime/audit/human_queue",
            },
            {
                "id": "NEXT-003",
                "title": "PRD V1.0 重写",
                "assignee": "DOC-001",
                "phase": "Next Alpha Run",
                "status": "waiting",
                "artifact": "MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Alpha_Run_002/02_codex_project_pack_intake.md",
            },
            {
                "id": "NEXT-004",
                "title": "架构 ADR V1",
                "assignee": "ARC-001",
                "phase": "Next Alpha Run",
                "status": "waiting",
                "artifact": "MCP/02_Architecture",
            },
        ]
    for task in next_tasks:
        command = command_by_task.get(task["id"])
        if command:
            task["status"] = task_status_from_command(command)
            task["last_command"] = command
        else:
            task["last_command"] = None
    tasks.extend(next_tasks)
    return tasks


def task_status_from_command(command: dict[str, Any]) -> str:
    command_status = command.get("status")
    if command_status == "READY_FOR_SAFE_EXECUTION":
        return "ready"
    if command_status == "SAFE_EXECUTION_QUEUED":
        return "queued"
    if command_status in {"BLOCKED_PRODUCTION_DEFAULT_DENY", "REJECTED"}:
        return "blocked"
    if str(command_status).startswith("WAIT_"):
        return "gated"
    return "queued"


def build_timeline(invocations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    for item in invocations:
        timeline.append(
            {
                "id": item.get("id"),
                "sequence": item.get("sequence"),
                "run_name": item.get("run_name"),
                "agent_id": item.get("agent_id"),
                "agent": item.get("agent") or item.get("agent_id"),
                "provider_id": item.get("provider_id"),
                "status": item.get("status"),
                "task": item.get("task"),
                "artifact": item.get("artifact"),
                "mock": item.get("mock"),
                "simulated": item.get("simulated"),
                "codex_version": item.get("codex_version"),
            }
        )
    return timeline


def build_snapshot() -> dict[str, Any]:
    profiles = load_agent_profiles()
    metrics = load_metrics()
    queue = load_human_queue()
    invocations = load_provider_invocations()
    base_tasks = build_tasks([])
    commands = load_run_requests(base_tasks)
    providers = load_providers(invocations)
    agents = build_agents(profiles, metrics, queue, invocations)
    tasks = build_tasks(commands)
    completed = sum(1 for task in tasks if task["status"] == "complete")

    worker_summary = load_worker_summary()
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project": {
            "name": "株洲物业监管平台",
            "memory_path": str(PROJECT_MEMORY_DIR.relative_to(REPO_ROOT)),
            "runtime_baseline": "OMCF Runtime V2.6 frozen",
            "dashboard": "OMCF Dashboard Alpha",
        },
        "agents": agents,
        "tasks": tasks,
        "task_summary": {
            "total": len(tasks),
            "complete": completed,
            "waiting": sum(1 for task in tasks if task["status"] == "waiting"),
            "human": sum(1 for task in tasks if task["status"] == "human"),
            "completion_rate": round(completed / len(tasks), 4) if tasks else 0,
        },
        "human_queue": queue,
        "metrics": list(metrics.values()),
        "providers": providers,
        "provider_invocations": invocations,
        "timeline": build_timeline(invocations),
        "commands": commands[-20:],
        "safe_execution_summary": {
            "ready": sum(1 for command in commands if command.get("status") == "READY_FOR_SAFE_EXECUTION"),
            "waiting_human": sum(1 for command in commands if command.get("status") == "WAIT_HUMAN_APPROVAL"),
            "waiting_audit": sum(1 for command in commands if command.get("status") == "WAIT_AUDIT_PASS"),
            "queued": sum(1 for command in commands if command.get("status") == "SAFE_EXECUTION_QUEUED"),
            "blocked_production": sum(
                1 for command in commands if command.get("status") == "BLOCKED_PRODUCTION_DEFAULT_DENY"
            ),
        },
        "worker_summary": worker_summary,
    }


def load_worker_summary() -> dict[str, Any]:
    worker_log = STATE_DIR / "safe_worker_events.jsonl"
    rows = read_jsonl(worker_log)
    return {
        "events": len(rows),
        "completed": sum(1 for row in rows if row.get("status") == "WORKER_COMPLETED"),
        "rejected": sum(1 for row in rows if row.get("status") == "WORKER_REJECTED"),
        "failed": sum(1 for row in rows if row.get("status") == "WORKER_FAILED"),
        "dry_run_pass": sum(1 for row in rows if row.get("status") == "WORKER_DRY_RUN_PASS"),
        "last_event": rows[-1] if rows else None,
    }


def find_agent(agent_id: str) -> dict[str, Any] | None:
    return next((agent for agent in build_snapshot()["agents"] if agent["id"] == agent_id), None)


def find_task(task_id: str) -> dict[str, Any] | None:
    return next((task for task in build_snapshot()["tasks"] if task["id"] == task_id), None)


def record_decision_for_item(item_key: str, decision: str, note: str | None = None) -> dict[str, Any]:
    allowed = {"approve", "reject", "return"}
    if decision not in allowed:
        raise HTTPException(status_code=400, detail="decision must be approve, reject, or return")

    queue_items = {queue_item_key(item): item for item in load_human_queue()}
    if item_key not in queue_items:
        raise HTTPException(status_code=404, detail="human queue item not found")

    row = {
        "item_key": item_key,
        "decision": decision,
        "note": note or "",
        "decided_at": datetime.now().isoformat(timespec="seconds"),
        "decider": "King Xu",
        "dashboard_alpha_only": True,
        "runtime_queue_mutated": False,
    }
    append_jsonl(DECISION_LOG, row)
    return row


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/snapshot")
def snapshot() -> dict[str, Any]:
    return build_snapshot()


@app.post("/api/runs/start")
def start_run(request: StartRunRequest) -> dict[str, Any]:
    snapshot_data = build_snapshot()
    tasks = {task["id"]: task for task in snapshot_data["tasks"]}
    agents = {agent["id"]: agent for agent in snapshot_data["agents"]}

    task = tasks.get(request.task_id or "") if request.task_id else None
    agent = agents.get(request.agent_id or "") if request.agent_id else None
    if request.task_id and not task:
        raise HTTPException(status_code=404, detail="task_id not found")
    if request.agent_id and not agent:
        raise HTTPException(status_code=404, detail="agent_id not found")

    resolved_agent_id = request.agent_id or (task or {}).get("assignee") or "PM-001"
    resolved_agent = agents.get(resolved_agent_id, {})
    command_id = f"DASH-RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:6]}"
    row = {
        "command_id": command_id,
        "type": "RUN_START_REQUEST",
        "status": "QUEUED_FOR_RUNTIME",
        "project": request.project or snapshot_data["project"]["name"],
        "task_id": request.task_id or "NEXT-001",
        "task_title": request.title or (task or {}).get("title") or "Dashboard requested run",
        "agent_id": resolved_agent_id,
        "agent": resolved_agent.get("nickname", resolved_agent_id),
        "note": request.note or "",
        "created_by": "King Xu",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dashboard_alpha_only": True,
        "runtime_core_changed": False,
        "runtime_handoff_status": "PENDING_OPERATOR_OR_EXISTING_RUNTIME_ADAPTER",
        "suggested_next_step": "Hand this command to the existing OMCF Runtime or Codex provider adapter after human confirmation.",
    }
    append_jsonl(RUN_REQUEST_LOG, row)
    enriched = enrich_command(row, [], list(tasks.values()))
    append_jsonl(
        SAFE_EXECUTION_EVENT_LOG,
        {
            "command_id": command_id,
            "type": "DRY_RUN_COMPLETED",
            "status": enriched["dry_run"]["status"],
            "task_type": enriched["dry_run"]["task_type"],
            "risk": enriched["dry_run"]["risk"],
            "recorded_at": datetime.now().isoformat(timespec="seconds"),
            "dashboard_alpha_only": True,
        },
    )
    return {"ok": True, "command": enrich_command(row, load_safe_execution_events().get(command_id, []), list(tasks.values()))}


def get_command_or_404(command_id: str) -> dict[str, Any]:
    commands = load_run_requests(build_tasks([]))
    command = next((item for item in commands if item.get("command_id") == command_id), None)
    if not command:
        raise HTTPException(status_code=404, detail="command_id not found")
    return command


def record_command_event(command_id: str, event_type: str, note: str | None = None) -> dict[str, Any]:
    command = get_command_or_404(command_id)
    row = {
        "command_id": command_id,
        "type": event_type,
        "note": note or "",
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "recorded_by": "King Xu" if "HUMAN" in event_type else "赵云",
        "dashboard_alpha_only": True,
        "runtime_core_changed": False,
    }
    append_jsonl(SAFE_EXECUTION_EVENT_LOG, row)
    return enrich_command(command, load_safe_execution_events().get(command_id, []), build_tasks([]))


@app.post("/api/commands/{command_id}/dry-run")
def command_dry_run(command_id: str, request: CommandEventRequest | None = None) -> dict[str, Any]:
    command = get_command_or_404(command_id)
    row = {
        "command_id": command_id,
        "type": "DRY_RUN_COMPLETED",
        "status": command["dry_run"]["status"],
        "task_type": command["dry_run"]["task_type"],
        "risk": command["dry_run"]["risk"],
        "note": (request.note if request else None) or "Dry run refreshed from Command Center",
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "dashboard_alpha_only": True,
    }
    append_jsonl(SAFE_EXECUTION_EVENT_LOG, row)
    return {"ok": True, "command": get_command_or_404(command_id)}


@app.post("/api/commands/{command_id}/approve")
def approve_command(command_id: str, request: CommandEventRequest | None = None) -> dict[str, Any]:
    command = record_command_event(command_id, "HUMAN_APPROVAL_GRANTED", (request.note if request else None))
    return {"ok": True, "command": command}


@app.post("/api/commands/{command_id}/reject")
def reject_command(command_id: str, request: CommandEventRequest | None = None) -> dict[str, Any]:
    command = record_command_event(command_id, "HUMAN_REJECTED", (request.note if request else None))
    return {"ok": True, "command": command}


@app.post("/api/commands/{command_id}/audit-pass")
def audit_pass_command(command_id: str, request: CommandEventRequest | None = None) -> dict[str, Any]:
    current = get_command_or_404(command_id)
    missing = current.get("missing_gates", [])
    if "production_whitelist" in missing:
        raise HTTPException(status_code=409, detail="Production whitelist is required before audit pass.")
    if "human_approval" in missing:
        raise HTTPException(status_code=409, detail="King Xu approval is required before audit pass.")
    command = record_command_event(command_id, "AUDIT_PASSED", (request.note if request else None))
    return {"ok": True, "command": command}


@app.post("/api/commands/{command_id}/execute")
def execute_command(command_id: str, request: CommandEventRequest | None = None) -> dict[str, Any]:
    command = get_command_or_404(command_id)
    if command.get("status") != "READY_FOR_SAFE_EXECUTION":
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Command is not ready for safe execution.",
                "status": command.get("status"),
                "missing_gates": command.get("missing_gates", []),
            },
        )
    packet = build_safe_execution_packet(command)
    row = {
        "command_id": command_id,
        "type": "SAFE_EXECUTION_QUEUED",
        "status": "QUEUED_FOR_RUNTIME_DISPATCH",
        "packet_path": packet["packet_path"],
        "note": (request.note if request else None) or "",
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "dashboard_alpha_only": True,
        "runtime_core_changed": False,
    }
    append_jsonl(SAFE_EXECUTION_EVENT_LOG, row)
    append_jsonl(SAFE_EXECUTION_QUEUE_LOG, row)
    return {"ok": True, "command": get_command_or_404(command_id), "packet": packet}


@app.post("/api/worker/run-once")
def run_worker_once(request: WorkerRunRequest) -> dict[str, Any]:
    from OMCF_Runtime.dashboard.safe_worker import run_once

    result = run_once(
        command_id=request.command_id,
        dry_run=request.dry_run,
        limit=max(1, min(request.limit, 5)),
        timeout_seconds=max(30, min(request.timeout_seconds, 600)),
    )
    return {"ok": True, "worker": result, "summary": load_worker_summary()}


@app.get("/api/agents/{agent_id}/timeline")
def agent_timeline(agent_id: str) -> dict[str, Any]:
    snapshot_data = build_snapshot()
    agent = next((item for item in snapshot_data["agents"] if item["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="agent_id not found")
    timeline = [item for item in snapshot_data["timeline"] if item.get("agent_id") == agent_id]
    commands = [item for item in snapshot_data["commands"] if item.get("agent_id") == agent_id]
    return {
        "agent": agent,
        "timeline": timeline,
        "commands": commands,
        "metrics": agent.get("metrics", {}),
    }


@app.get("/api/tasks/{task_id}/trace")
def task_trace(task_id: str) -> dict[str, Any]:
    snapshot_data = build_snapshot()
    task = next((item for item in snapshot_data["tasks"] if item["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="task_id not found")
    artifact = task.get("artifact") or ""
    artifact_name = Path(artifact).name
    timeline = [
        item
        for item in snapshot_data["timeline"]
        if item.get("agent_id") == task.get("assignee")
        or (artifact_name and artifact_name in str(item.get("artifact", "")))
    ]
    commands = [item for item in snapshot_data["commands"] if item.get("task_id") == task_id]
    return {
        "task": task,
        "assignee": find_agent(task.get("assignee", "")),
        "timeline": timeline,
        "commands": commands,
        "artifact_exists": artifact_exists(artifact),
    }


@app.post("/api/human-queue/{item_key:path}/decision")
def record_queue_decision(item_key: str, decision: QueueDecision) -> dict[str, Any]:
    row = record_decision_for_item(item_key, decision.decision, decision.note)
    return {"ok": True, "decision": row}


@app.post("/api/human-queue/{item_key:path}/approve")
def approve_queue_item(item_key: str) -> dict[str, Any]:
    row = record_decision_for_item(item_key, "approve", "Approved from Command Center Alpha")
    return {"ok": True, "decision": row}


@app.post("/api/human-queue/{item_key:path}/reject")
def reject_queue_item(item_key: str) -> dict[str, Any]:
    row = record_decision_for_item(item_key, "reject", "Rejected from Command Center Alpha")
    return {"ok": True, "decision": row}


@app.websocket("/ws")
async def websocket_snapshot(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(build_snapshot())
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        return
