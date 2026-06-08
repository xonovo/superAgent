# OMC-OS Workbench Alpha

```text
OMCF = OneMan AI Company Framework
OMC-OS = OneMan AI Company Operating System
```

OMC-OS Workbench Alpha 是 OMC-OS 的用户界面层，也就是 AI Agent IDE
的第一版产品形态。

当前产品层次：

1. OMCF: 公司治理层，负责组织、协议、审计、知识、记忆。
2. OMCF Runtime: 执行层，负责 Task Engine、Provider、Worker、Human Queue。
3. OMC-OS Workbench: 用户界面层，负责 Workspace、Projects、Agent Pool、Command Center。

当前 UI 已升级为 OMC-OS Workbench Alpha。它还不是完整 IDE，但已经具备
AI Agent IDE 的第一版外壳：

- Workspace 工作区。
- Projects 真实项目列表。
- Agent Pool 公司级智能体池。
- Project Binding 项目上下文绑定。
- Project Explorer 项目资源管理器。
- Agent Console 智能体控制台。
- Execution Terminal 执行终端。
- Command Center 安全指挥台。
- Trace / Human Queue / Metrics / Provider 调用链。

OMC-OS Workbench Alpha is the project-centered AI Agent IDE layer for the
existing OMCF Runtime.

It does not introduce a new Runtime version, role, or protocol. It reads the
current Runtime, Provider, Audit, Metrics, and Project Memory artifacts and
renders them as an IDE-style workbench.

## Command Center Alpha

The dashboard exposes these local APIs:

```text
POST /api/runs/start
POST /api/commands/{command_id}/dry-run
POST /api/commands/{command_id}/approve
POST /api/commands/{command_id}/reject
POST /api/commands/{command_id}/audit-pass
POST /api/commands/{command_id}/execute
POST /api/projects/draft
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
9. Record a new-project draft without creating an empty project directory.

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
