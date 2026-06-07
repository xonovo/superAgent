# OMCF Dashboard Alpha

OMCF Dashboard Alpha is the observability layer for the existing OMCF Runtime.

It does not introduce a new Runtime version, role, or protocol. It reads the
current Runtime, Provider, Audit, Metrics, and Project Memory artifacts and
renders them as a control-center UI.

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
- They do not approve, reject, delete, or mutate the real Runtime queue files.
- The dashboard is read-mostly and can be safely used while OMCF Runtime V2.6
  remains frozen.
