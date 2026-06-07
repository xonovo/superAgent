# Project Memory

本目录用于管理项目级长期记忆。仓颉负责全局记忆，但每个项目必须拥有自己的记忆空间。

## 标准项目记忆

每个项目必须维护：

1. Decision Log
2. Architecture Log
3. Risk Log
4. Failure Log
5. Lessons Learned

## 项目创建规则

OMCF 不预设具体项目槽位。任何项目记忆目录都必须在项目正式启动时，根据 `PROJECT_MEMORY_TEMPLATE.md` 按需创建。

示例：

```text
Project_Memory/
└── <Project_Code>/
    ├── README.md
    ├── decision_log.md
    ├── architecture_log.md
    ├── risk_log.md
    ├── failure_log.md
    └── lessons_learned.md
```

## 强制规则

1. 项目启动前必须检索对应 Project Memory。
2. 项目结束后必须更新 Lessons Learned。
3. 审计失败必须写入 Failure Log。
4. 架构变化必须写入 Architecture Log。
5. 重大决策必须写入 Decision Log。
6. 未正式启动的项目不得提前创建项目记忆槽位。
