# 第二阶段生成计划

第二阶段在第一阶段文档体系完成后启动。

## 生成目标

第二阶段由女娲、诸葛亮和墨子基于 MCP 文档自动生成：

1. 任务树
2. 任务依赖图
3. 里程碑
4. 开发计划
5. 风险清单
6. 专家任务清单

## 前置条件

1. `MCP/MCP_V2_MASTER_CONTROL_PROTOCOL.md` 已确认。
2. `MCP/AGENT_ROLE_MATRIX.md` 已确认。
3. 每个领域目录的核心文档已至少达到 `DRAFT`。
4. 产品、架构、数据、API、AI、AOEM、数学、新语言、审计和部署之间的边界已明确。

## 生成顺序

```text
产品模块清单
  -> 架构模块清单
    -> 数据域清单
      -> API 清单
        -> UI 页面清单
          -> AI / AOEM / 数学 / 新语言专项清单
            -> 开发任务树
              -> 任务依赖图
                -> 里程碑
                  -> 风险清单
```

## 输出文件建议

- `MCP/task_tree.md`
- `MCP/task_dependency_graph.md`
- `MCP/milestone_plan.md`
- `MCP/development_plan.md`
- `MCP/risk_register.md`
- `MCP/expert_task_register.md`
