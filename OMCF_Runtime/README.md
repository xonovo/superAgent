# OMCF Runtime

OMCF Runtime 是 OMCF 从“组织制度”进入“可运行组织”的执行引擎。

当前目标不是写业务代码，而是跑通最小组织链路：

```text
项目启动
  -> 女娲接收请求
  -> 诸葛亮生成任务树
  -> 墨子生成架构树
  -> 嬴政生成文档树
  -> 赵云生成审计报告
```

## 目录

```text
OMCF_Runtime/
├── agents      Agent Registry
├── tasks       任务运行输出
├── memory      Runtime 记忆适配层
├── knowledge   Runtime 知识适配层
├── runtime     执行引擎
└── audit       Runtime 审计适配层
```

## Runtime V1

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

V1 生成项目启动链路的结构化文件。

## Runtime V2

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

V2 增加 Tool Layer：

1. 本地知识库检查。
2. 项目记忆模板检查。
3. Agent 调用包生成。
4. 工具调用日志。
5. 赵云审计门禁。

查看工具注册表：

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-tools
```

## Runtime V2.5

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2-5 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

V2.5 增加 Provider Layer 和 Human Approval Layer：

1. Agent Profile 与执行 Provider 解耦。
2. Provider Registry 决定 Codex、GPT、Claude、本地模型或 AOEM 由谁执行。
3. Provider Route 进入工具调用日志。
4. 敏感范围进入 `WAIT_HUMAN_APPROVAL`，不视为失败。
5. 缺文件、工具失败才进入 `AUDIT_FAIL`。

查看 Provider 注册表：

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-providers
```

触发人工审批示例：

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2-5 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台" --sensitive-scope database_schema --sensitive-scope aoem_core_logic
```

## Runtime V2.6

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2-6 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

V2.6 增加三项能力：

1. Provider Adapter：启用的 provider 会产出 `PROVIDER_EXECUTED`。
2. Human Queue：人工审批请求会写入本地队列。
3. Metrics Center：每次运行会生成运行指标，并更新本地 Agent 指标。

查看 Human Queue：

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-human-queue
```

查看 Metrics：

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-metrics
```

运行产物会写入：

```text
OMCF_Runtime/tasks/runs/
```

`runs/` 默认不提交到 Git，用于保存本地试跑结果。

## Runtime 边界

1. Runtime 不是 AI，最终干活的仍然是 Codex、GPT、AOEM 或其他外部工具。
2. Runtime 不直接写业务代码。
3. Runtime 不自动修改 MCP 制度层。
4. Runtime 使用 MCP 文档作为制度来源。
5. V2 只记录外部 Agent 调用合同，不直接调用远程模型。
6. V2.5 只定义 Provider 合同和人工审批状态，不保存 API Key。
7. V2.6 只执行已启用的本地 provider adapter；外部 API provider 未配置前不会伪造成功。
