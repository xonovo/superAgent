from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

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


def build_tasks() -> list[dict[str, Any]]:
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
    tasks = []
    for task_id, title, assignee, phase, artifact in specs:
        exists = artifact_exists(artifact)
        tasks.append(
            {
                "id": task_id,
                "title": title,
                "assignee": assignee,
                "phase": phase,
                "status": "complete" if exists else "waiting",
                "artifact": artifact,
            }
        )

    tasks.extend(
        [
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
    )
    return tasks


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
    providers = load_providers(invocations)
    agents = build_agents(profiles, metrics, queue, invocations)
    tasks = build_tasks()
    completed = sum(1 for task in tasks if task["status"] == "complete")

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
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/snapshot")
def snapshot() -> dict[str, Any]:
    return build_snapshot()


@app.post("/api/human-queue/{item_key:path}/decision")
def record_queue_decision(item_key: str, decision: QueueDecision) -> dict[str, Any]:
    allowed = {"approve", "reject", "return"}
    if decision.decision not in allowed:
        raise HTTPException(status_code=400, detail="decision must be approve, reject, or return")

    queue_items = {queue_item_key(item): item for item in load_human_queue()}
    if item_key not in queue_items:
        raise HTTPException(status_code=404, detail="human queue item not found")

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "item_key": item_key,
        "decision": decision.decision,
        "note": decision.note or "",
        "decided_at": datetime.now().isoformat(timespec="seconds"),
        "decider": "King Xu",
        "dashboard_alpha_only": True,
    }
    with DECISION_LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")
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
