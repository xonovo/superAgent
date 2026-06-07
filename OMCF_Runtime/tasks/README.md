# Runtime Tasks

本目录用于保存 OMCF Runtime 的任务定义和运行输出。

运行结果默认输出到：

```text
OMCF_Runtime/tasks/runs/
```

`runs/` 是本地运行产物，不提交到 Git。

## Runtime V2.5 Status

Runtime V2.5 introduces three important statuses:

1. `READY_FOR_PROVIDER`: agent packet has been routed to an enabled provider contract.
2. `WAIT_ADAPTER_CONFIGURATION`: provider exists but its adapter is not enabled.
3. `WAIT_HUMAN_APPROVAL`: protected scope requires King Xu approval before execution continues.
4. `PROVIDER_EXECUTED`: enabled provider adapter executed and returned an auditable result.
5. `READY_FOR_CODEX_ADAPTER`: provider.codex is available and requires explicit `invoke-codex` task execution.
