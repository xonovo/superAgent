from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
HOME_ROOT = Path.home()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def sanitize_text(value: str) -> str:
    result = value.replace(str(REPO_ROOT), "<REPO_ROOT>")
    result = result.replace(str(HOME_ROOT), "<HOME>")
    result = result.replace(str(REPO_ROOT).replace("\\", "\\\\"), "<REPO_ROOT>")
    result = result.replace(str(HOME_ROOT).replace("\\", "\\\\"), "<HOME>")
    return result


def tail_text(value: str, max_chars: int = 4000) -> str:
    value = sanitize_text(value)
    if len(value) <= max_chars:
        return value
    return value[-max_chars:]


def codex_version() -> str:
    codex_path = shutil.which("codex")
    if not codex_path:
        return "codex_not_found"
    result = subprocess.run(
        [codex_path, "--version"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    return result.stdout.strip() or result.stderr.strip() or "unknown"


def invoke_codex(task_file: Path, output_dir: Path, sandbox: str, timeout_seconds: int) -> dict[str, Any]:
    codex_path = shutil.which("codex")
    started_at = now_iso()
    output_dir.mkdir(parents=True, exist_ok=True)

    task = read_json(task_file)
    prompt = str(task.get("prompt", "")).strip()
    if not prompt:
        raise ValueError(f"Task file has no prompt: {task_file}")

    if codex_path is None:
        payload = {
            "status": "CODEX_CLI_MISSING",
            "started_at": started_at,
            "finished_at": now_iso(),
            "task_file": rel_path(task_file),
            "output_dir": rel_path(output_dir),
        }
        write_json(output_dir / "codex_adapter_result.json", payload)
        return payload

    output_name = str(task.get("output_name", "codex_provider_output.md"))
    last_message_path = output_dir / output_name
    command = [
        codex_path,
        "exec",
        "--ephemeral",
        "--sandbox",
        sandbox,
        "-C",
        str(REPO_ROOT),
        "--output-last-message",
        str(last_message_path),
        prompt,
    ]

    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
    )
    finished_at = now_iso()

    output_exists = last_message_path.exists()
    payload = {
        "status": "PROVIDER_EXECUTED" if result.returncode == 0 and output_exists else "PROVIDER_FAILED",
        "provider_id": "provider.codex",
        "adapter": "OMCF_Runtime/providers/codex/codex_adapter.py",
        "codex_cli": "codex",
        "codex_cli_detected": True,
        "codex_version": codex_version(),
        "task_id": task.get("task_id", ""),
        "agent_id": task.get("agent_id", ""),
        "project": task.get("project", ""),
        "mock": False,
        "simulated": False,
        "sandbox": sandbox,
        "started_at": started_at,
        "finished_at": finished_at,
        "returncode": result.returncode,
        "task_file": rel_path(task_file),
        "output_dir": rel_path(output_dir),
        "last_message_path": rel_path(last_message_path),
        "stdout_tail": tail_text(result.stdout),
        "stderr_tail": tail_text(result.stderr),
    }
    write_json(output_dir / "codex_adapter_result.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="OMCF Codex provider adapter")
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--sandbox", default="read-only", choices=["read-only", "workspace-write", "danger-full-access"])
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()

    try:
        payload = invoke_codex(
            task_file=Path(args.task_file).resolve(),
            output_dir=Path(args.output_dir).resolve(),
            sandbox=args.sandbox,
            timeout_seconds=args.timeout_seconds,
        )
    except Exception as exc:
        payload = {
            "status": "PROVIDER_FAILED",
            "provider_id": "provider.codex",
            "adapter": "OMCF_Runtime/providers/codex/codex_adapter.py",
            "mock": False,
            "simulated": False,
            "error": f"{type(exc).__name__}: {exc}",
            "finished_at": now_iso(),
        }
        output_dir = Path(args.output_dir).resolve()
        write_json(output_dir / "codex_adapter_result.json", payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "PROVIDER_EXECUTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
