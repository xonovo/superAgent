# OMCF Dashboard Alpha

OMCF Dashboard Alpha is the observability and command layer for the existing
OMCF Runtime.

It does not introduce a new Runtime version, role, or protocol. It reads the
current Runtime, Provider, Audit, Metrics, and Project Memory artifacts and
renders them as a control-center UI.

## Command Center Alpha

The dashboard exposes these local APIs:

```text
POST /api/runs/start
POST /api/commands/{command_id}/dry-run
POST /api/commands/{command_id}/approve
POST /api/commands/{command_id}/reject
POST /api/commands/{command_id}/audit-pass
POST /api/commands/{command_id}/execute
POST /api/worker/run-once
POST /api/human-queue/{id}/approve
POST /api/human-queue/{id}/reject
GET  /api/agents/{agent_id}/timeline
GET  /api/tasks/{task_id}/trace
```

The UI uses them to:

1. Create a dashboard run-start command.
2. Run a dry-run risk classification.
3. Record King Xu approval or rejection.
4. Record Zhao Yun audit pass.
5. Queue a command for safe execution only after gates pass.
6. Let Safe Execution Worker Alpha process eligible low-risk commands.
7. Inspect an agent timeline.
8. Inspect a task trace.

## Safe Execution Gates

Every command starts with a dry run. The safe execution policy is:

| Task Type | Required Gates |
|---|---|
| Document task | Dry Run |
| Code task | Dry Run, Zhao Yun Audit |
| Database / bank / AOEM / deployment task | Dry Run, King Xu Approval, Zhao Yun Audit |
| Production task | Denied by default; requires a manual production whitelist, King Xu Approval, and Zhao Yun Audit |

`execute` writes a safe execution packet and queue record under
`OMCF_Runtime/dashboard/state/`. It does not directly run production commands.

## Safe Execution Worker Alpha

Worker Alpha only processes commands that are already in `SAFE_EXECUTION_QUEUED`
state and still pass the worker allowlist.

Allowed:

- Generate documents.
- Call Codex in `read-only` sandbox to generate a plan or proposal.
- Write the worker output and Zhao Yun audit note into Project Memory.

Forbidden:

- Database changes.
- Bank/payment interfaces.
- AOEM core/runtime operations.
- Production deployment.
- File deletion or destructive commands.

The worker writes outputs to:

```text
MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Safe_Execution_Worker_Alpha/
```

It also records worker events under:

```text
OMCF_Runtime/dashboard/state/
```

## Run

```powershell
python -m pip install -r OMCF_Runtime/dashboard/requirements.txt
python -m uvicorn OMCF_Runtime.dashboard.server:app --host 127.0.0.1 --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

Chinese beginner guide:

```text
OMCF_Runtime/dashboard/USER_GUIDE_zh-CN.md
```

## Alpha Boundaries

- Human Queue buttons write only to `OMCF_Runtime/dashboard/state/`.
- Run-start buttons write only to `OMCF_Runtime/dashboard/state/`.
- Safe Execution buttons write only to `OMCF_Runtime/dashboard/state/`.
- Worker buttons execute only allowlisted low-risk document tasks.
- These buttons do not approve, reject, delete, execute, or mutate real Runtime
  queue files.
- They do not run database, bank, AOEM, deployment, or production commands.
- The dashboard can be safely used while OMCF Runtime V2.6 remains frozen.
