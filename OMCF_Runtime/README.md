# OMCF Runtime V1

OMCF Runtime V1 是 OMCF 从“组织制度”进入“可运行组织”的第一版执行引擎。

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

## 最小运行命令

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

运行产物会写入：

```text
OMCF_Runtime/tasks/runs/
```

`runs/` 默认不提交到 Git，用于保存本地试跑结果。

## V1 边界

1. V1 不接外部 LLM。
2. V1 不执行业务代码。
3. V1 不自动修改 MCP 制度层。
4. V1 只生成项目启动链路的结构化产物。
5. V1 使用 MCP 文档作为制度来源。
