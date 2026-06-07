# superAgent

This repository contains the OMCF documentation layer and the first minimal OMCF Runtime.

## Runtime V1

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

## Runtime V2

Runtime V2 adds the first Tool Layer contract. It does not pretend to be an AI model. It records auditable tool calls and Codex/GPT agent-call packets so external adapters can execute real work later.

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-tools
```
