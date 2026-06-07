# 03 Database

本目录负责数据模型、数据字典、数据库迁移、存储过程和性能优化。

## 数据库工作原则

1. 数据字典先于建表。
2. 数据治理口径先于迁移。
3. 迁移脚本必须可回滚。
4. 核心字段必须明确来源、含义、约束和审计要求。
5. 资金、产权、身份证、手机号、银行卡等敏感数据必须标识安全等级。

## 必备文档

- `data_dictionary.md`：数据字典。
- `erd.md`：实体关系说明。
- `migration_strategy.md`：迁移策略。
- `performance_strategy.md`：性能策略。

## 责任角色

- 主责：Database Codex
- 协作：Data Governance Codex、Backend Codex、Auditor Codex

