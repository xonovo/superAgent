# Codex Provider Adapter

Codex is the primary software-development provider for OMCF Alpha.

Runtime V2.6 remains frozen. This adapter is an execution adapter improvement, not a Runtime version upgrade.

## Adapter

```text
OMCF_Runtime/providers/codex/codex_adapter.py
```

The adapter calls:

```powershell
codex exec --ephemeral --sandbox read-only -C <repo> --output-last-message <artifact> <prompt>
```

## Runtime Route

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py invoke-codex --task-file <task.json> --output-dir <dir>
```

## Guarantees

1. It uses the real local Codex CLI.
2. It writes a provider result JSON.
3. It writes the final Codex message as an artifact.
4. It records `mock=false` and `simulated=false`.
5. It defaults to read-only sandbox execution.

The adapter does not bind OMCF agents permanently to Codex. Agents remain profiles; Codex is one provider implementation.
