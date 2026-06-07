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
POST /api/human-queue/{id}/approve
POST /api/human-queue/{id}/reject
GET  /api/agents/{agent_id}/timeline
GET  /api/tasks/{task_id}/trace
```

The UI uses them to:

1. Create a dashboard run-start command.
2. Record approve / reject / return decisions.
3. Inspect an agent timeline.
4. Inspect a task trace.

## Run

```powershell
python -m pip install -r OMCF_Runtime/dashboard/requirements.txt
python -m uvicorn OMCF_Runtime.dashboard.server:app --host 127.0.0.1 --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

## Alpha Boundaries

- Human Queue buttons write only to `OMCF_Runtime/dashboard/state/`.
- Run-start buttons write only to `OMCF_Runtime/dashboard/state/`.
- These buttons do not approve, reject, delete, execute, or mutate real Runtime
  queue files.
- They do not run database, bank, AOEM, deployment, or production commands.
- The dashboard can be safely used while OMCF Runtime V2.6 remains frozen.
