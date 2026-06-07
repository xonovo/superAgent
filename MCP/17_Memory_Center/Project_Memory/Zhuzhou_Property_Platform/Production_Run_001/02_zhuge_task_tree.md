# 诸葛亮任务树

## Project

- Project: 株洲物业监管平台
- Run ID: OMCF-PRUN-001
- Provider: provider.codex.manual
- Provider status: PROVIDER_EXECUTED
- Phase: Phase-1 文档建设与系统边界确认

## Task Tree

| Task ID | Task | Owner | Output | Gate | Status |
|---|---|---|---|---|---|
| ZZW-001 | 项目启动与范围确认 | 女娲 / 诸葛亮 | Run Manifest | ZhaoYun audit | DONE |
| ZZW-002 | 任务树生成 | 诸葛亮 | Task Tree | Capability Matrix | DONE |
| ZZW-003 | 架构树生成 | 墨子 | Architecture Tree | Architecture boundary check | DONE |
| ZZW-004 | PRD V0.1 生成 | 嬴政 | PRD | Product completeness check | DONE |
| ZZW-005 | 数据库边界分析 | 鲁班七号 | Database Analysis | No schema change without approval | DONE |
| ZZW-006 | 数据质量分析 | 项羽 | Data Quality Analysis | Data governance check | DONE |
| ZZW-007 | 启动审计 | 赵云 | Audit Report | PASS required | DONE |
| ZZW-008 | 原始资料补齐 | King Xu / 诸葛亮 | Project Pack V1 | Human input required | PENDING |
| ZZW-009 | 现有系统与数据库盘点 | 鲁班七号 / 张飞 | Inventory Report | Human approval before access | PENDING |
| ZZW-010 | 外部接口清单确认 | 刘备 | API Inventory | Bank/payment/property interfaces require approval | PENDING |

## Dependency Graph

```text
King Xu instruction
  -> Project startup
    -> Task tree
      -> Architecture tree
        -> PRD
          -> Database analysis
            -> Data quality analysis
              -> ZhaoYun audit
                -> Project Pack completion
```

## Phase-1 Milestones

1. Freeze Runtime V2.6 as Control Plane baseline.
2. Complete Production Run 001 startup artifacts.
3. Collect real project materials from King Xu.
4. Inventory historical systems and databases.
5. Confirm external interface boundaries.
6. Produce PRD V1.0 after source material confirmation.
7. Enter database design only after human confirmation.

## Risk Register

| Risk | Level | Owner | Mitigation |
|---|---|---|---|
| Source project materials are incomplete | High | 诸葛亮 | Keep current PRD at V0.1 and mark assumptions |
| Historical database structure unknown | High | 鲁班七号 | Inventory first; no DDL or migration |
| Bank or fund interfaces may be sensitive | High | 刘备 / 赵云 | Require King Xu approval |
| Data quality may be inconsistent across systems | High | 项羽 | Run staged quality profiling before cleaning |
| AI output may be mistaken for decision authority | Medium | 王昭君 / 赵云 | AI output must be advisory and auditable |

## Next Action

King Xu provides the first real Project Pack:

1. Existing system description.
2. Existing database inventory or screenshots.
3. Known business departments and user roles.
4. External interface list.
5. Data sample policy.
6. Deployment environment constraints.
