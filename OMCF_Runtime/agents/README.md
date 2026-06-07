# Agent Registry

本目录是 OMCF Runtime V1 的 Agent 注册中心。

每个 Agent 使用简化 YAML 描述：

```yaml
id: PM-001
name: ZhugeLiang
nickname: 诸葛亮
role: Project Manager
capabilities:
  - task_tree_generation
knowledge:
  - MCP/PROJECT_PACK_TEMPLATE.md
```

Runtime V1 只读取必要字段，不依赖外部 YAML 库。
