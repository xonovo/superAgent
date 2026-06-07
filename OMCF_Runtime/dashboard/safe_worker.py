from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from OMCF_Runtime.dashboard import server
from OMCF_Runtime.providers.codex.codex_adapter import invoke_codex


WORKER_LOG = server.STATE_DIR / "safe_worker_events.jsonl"
DEFAULT_MEMORY_RUN_DIR = (
    server.PROJECT_MEMORY_DIR / "Safe_Execution_Worker_Alpha"
)

ALLOWED_TASK_TYPES = {"document"}
ALLOWED_EXECUTION_MODES = {"safe_queue_document"}
FORBIDDEN_TERMS = {
    "aoem",
    "bank",
    "database",
    "db",
    "ddl",
    "delete",
    "deploy",
    "docker",
    "drop table",
    "gpu",
    "k8s",
    "payment",
    "prod",
    "production",
    "remove-item",
    "rm ",
    "schema",
    "sql",
    "银行",
    "支付",
    "数据库",
    "删除",
    "部署",
    "生产",
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(server.REPO_ROOT))
    except ValueError:
        return str(path)


def load_worker_events() -> list[dict[str, Any]]:
    return read_jsonl(WORKER_LOG)


def processed_command_ids() -> set[str]:
    return {
        row["command_id"]
        for row in load_worker_events()
        if row.get("status") in {"WORKER_COMPLETED", "WORKER_REJECTED"}
        and row.get("command_id")
    }


def queued_command_ids() -> list[str]:
    ids: list[str] = []
    for row in read_jsonl(server.SAFE_EXECUTION_QUEUE_LOG):
        command_id = row.get("command_id")
        if command_id:
            ids.append(command_id)
    return ids


def command_by_id(command_id: str) -> dict[str, Any] | None:
    for command in server.load_run_requests(server.build_tasks([])):
        if command.get("command_id") == command_id:
            return command
    return None


def command_safety(command: dict[str, Any]) -> dict[str, Any]:
    dry_run = command.get("dry_run", {})
    task_type = dry_run.get("task_type")
    execution_mode = dry_run.get("execution_mode")
    risk = dry_run.get("risk")
    text = " ".join(
        [
            str(command.get("task_title", "")),
            str(command.get("task_id", "")),
            str(command.get("agent_id", "")),
            str(command.get("note", "")),
        ]
    ).lower()
    forbidden_hits = sorted(term for term in FORBIDDEN_TERMS if term in text)
    reasons: list[str] = []

    if command.get("status") != "SAFE_EXECUTION_QUEUED":
        reasons.append("command is not in SAFE_EXECUTION_QUEUED state")
    if task_type not in ALLOWED_TASK_TYPES:
        reasons.append(f"task_type {task_type!r} is not allowed")
    if execution_mode not in ALLOWED_EXECUTION_MODES:
        reasons.append(f"execution_mode {execution_mode!r} is not allowed")
    if risk != "low":
        reasons.append(f"risk {risk!r} is not low")
    if forbidden_hits:
        reasons.append(f"forbidden terms detected: {', '.join(forbidden_hits)}")

    return {
        "allowed": not reasons,
        "reasons": reasons,
        "task_type": task_type,
        "execution_mode": execution_mode,
        "risk": risk,
        "forbidden_hits": forbidden_hits,
    }


def build_worker_prompt(command: dict[str, Any]) -> str:
    return f"""You are OMCF Safe Execution Worker Alpha.

Task:
{command.get("task_title")}

Agent:
{command.get("agent")} ({command.get("agent_id")})

Project:
{command.get("project")}

Safe boundary:
- Generate a Markdown document or project plan only.
- Do not modify repository files.
- Do not create code patches.
- Do not touch databases, bank/payment interfaces, AOEM runtime, deployment, production, credentials, or destructive operations.
- Produce concise deliverable sections: objective, assumptions, required inputs, execution steps, risks, and next audit checklist.
"""


def write_audit_report(output_dir: Path, command: dict[str, Any], codex_result: dict[str, Any]) -> Path:
    path = output_dir / "03_zhaoyun_worker_audit.md"
    lines = [
        "# ZhaoYun Worker Audit",
        "",
        "## Result",
        "",
        f"- Command ID: {command.get('command_id')}",
        f"- Task: {command.get('task_title')}",
        f"- Worker status: {'PASS' if codex_result.get('status') == 'PROVIDER_EXECUTED' else 'FAIL'}",
        f"- Provider status: {codex_result.get('status')}",
        f"- Sandbox: {codex_result.get('sandbox')}",
        "",
        "## Safety Boundary",
        "",
        "- Database changes: not executed",
        "- Bank/payment interfaces: not executed",
        "- AOEM core/runtime: not executed",
        "- Production deployment: not executed",
        "- File deletion: not executed",
        "",
        "## Memory Write",
        "",
        f"- Output directory: {display_path(output_dir)}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def reject(command_id: str, reasons: list[str], dry_run: bool) -> dict[str, Any]:
    row = {
        "command_id": command_id,
        "status": "WORKER_REJECTED",
        "reasons": reasons,
        "dry_run": dry_run,
        "recorded_at": now_iso(),
        "dashboard_alpha_only": True,
    }
    append_jsonl(WORKER_LOG, row)
    append_jsonl(
        server.SAFE_EXECUTION_EVENT_LOG,
        {
            "command_id": command_id,
            "type": "WORKER_REJECTED",
            "status": "WORKER_REJECTED",
            "reasons": reasons,
            "recorded_at": row["recorded_at"],
            "dashboard_alpha_only": True,
        },
    )
    return row


def execute_command(
    command: dict[str, Any],
    *,
    memory_root: Path = DEFAULT_MEMORY_RUN_DIR,
    dry_run: bool = False,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    command_id = command["command_id"]
    safety = command_safety(command)
    if not safety["allowed"]:
        return reject(command_id, safety["reasons"], dry_run=dry_run)

    output_dir = memory_root / command_id
    task_file = output_dir / "01_worker_codex_task.json"
    output_name = "02_worker_output.md"
    task_payload = {
        "task_id": command.get("task_id"),
        "command_id": command_id,
        "agent_id": command.get("agent_id"),
        "project": command.get("project"),
        "output_name": output_name,
        "prompt": build_worker_prompt(command),
    }

    if dry_run:
        row = {
            "command_id": command_id,
            "status": "WORKER_DRY_RUN_PASS",
            "safety": safety,
            "output_dir": display_path(output_dir),
            "recorded_at": now_iso(),
            "dashboard_alpha_only": True,
        }
        append_jsonl(WORKER_LOG, row)
        return row

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(task_file, task_payload)
    codex_result = invoke_codex(
        task_file=task_file,
        output_dir=output_dir,
        sandbox="read-only",
        timeout_seconds=timeout_seconds,
    )
    audit_path = write_audit_report(output_dir, command, codex_result)
    status = "WORKER_COMPLETED" if codex_result.get("status") == "PROVIDER_EXECUTED" else "WORKER_FAILED"
    row = {
        "command_id": command_id,
        "status": status,
        "provider_status": codex_result.get("status"),
        "output_dir": display_path(output_dir),
        "task_file": display_path(task_file),
        "output_file": codex_result.get("last_message_path"),
        "audit_file": display_path(audit_path),
        "recorded_at": now_iso(),
        "dashboard_alpha_only": True,
    }
    append_jsonl(WORKER_LOG, row)
    append_jsonl(
        server.SAFE_EXECUTION_EVENT_LOG,
        {
            "command_id": command_id,
            "type": status,
            "status": status,
            "output_dir": row["output_dir"],
            "audit_file": row["audit_file"],
            "recorded_at": row["recorded_at"],
            "dashboard_alpha_only": True,
        },
    )
    return row


def run_once(
    *,
    command_id: str | None = None,
    dry_run: bool = False,
    limit: int = 1,
    memory_root: Path = DEFAULT_MEMORY_RUN_DIR,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    processed = processed_command_ids()
    candidates = [command_id] if command_id else queued_command_ids()
    results: list[dict[str, Any]] = []
    for candidate_id in candidates:
        if not candidate_id or (candidate_id in processed and not dry_run):
            continue
        command = command_by_id(candidate_id)
        if not command:
            results.append(reject(candidate_id, ["command not found"], dry_run=dry_run))
        else:
            results.append(
                execute_command(
                    command,
                    memory_root=memory_root,
                    dry_run=dry_run,
                    timeout_seconds=timeout_seconds,
                )
            )
        if len(results) >= limit:
            break
    return {
        "status": "WORKER_IDLE" if not results else "WORKER_RAN",
        "dry_run": dry_run,
        "results": results,
        "recorded_at": now_iso(),
    }


def worker_summary() -> dict[str, Any]:
    events = load_worker_events()
    return {
        "events": len(events),
        "completed": sum(1 for event in events if event.get("status") == "WORKER_COMPLETED"),
        "rejected": sum(1 for event in events if event.get("status") == "WORKER_REJECTED"),
        "failed": sum(1 for event in events if event.get("status") == "WORKER_FAILED"),
        "dry_run_pass": sum(1 for event in events if event.get("status") == "WORKER_DRY_RUN_PASS"),
        "last_event": events[-1] if events else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="OMCF Safe Execution Worker Alpha")
    parser.add_argument("--command-id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()

    result = run_once(
        command_id=args.command_id,
        dry_run=args.dry_run,
        limit=args.limit,
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
