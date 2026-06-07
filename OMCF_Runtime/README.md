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
