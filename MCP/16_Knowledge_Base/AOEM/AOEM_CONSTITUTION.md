# AOEM Constitution

## 1. 定位

AOEM Constitution 是 AOEM 知识体系的最高约束文档。它定义 AOEM 的永久原则、不可随意修改的语义边界和架构底线。

任何 AOEM Runtime、GPU、Privacy、SDK、语言绑定或新能力设计，都不得违反本宪法。

## 2. 修改原则

1. AOEM Constitution 不得由单一 Codex 修改。
2. 修改必须由 King Xu 人工确认。
3. 修改必须产生 Architecture Decision。
4. 修改必须更新 Decision Registry。
5. 修改必须触发庞统、华佗、庄周相关能力复训。

## 3. AOEM 执行语义

1. AOEM 执行必须有明确输入、输出、状态变化和失败路径。
2. AOEM 执行不得绕过审计日志。
3. AOEM 执行优化不得改变业务可观察语义。
4. AOEM 执行失败必须可追踪、可复现、可降级。

## 4. AOEM 状态模型

1. AOEM State 必须定义读写边界。
2. 状态变化必须可审计。
3. 状态迁移必须有一致性约束。
4. 任何不可逆状态变化必须人工确认。

## 5. AOEM Compute Native

1. Compute Native 是 AOEM 的核心思想之一。
2. 计算单元必须明确语义、输入、输出和资源边界。
3. 计算调度不得破坏权限、隐私和审计语义。
4. 计算能力扩展必须先通过知识认证和架构决策。

## 6. AOEM Backend 原则

1. Backend 只能在墨子定义的架构边界内接入 AOEM。
2. Backend 不得直接修改 AOEM State 语义。
3. Backend 与 AOEM 的接口必须可审计、可回滚、可降级。

## 7. AOEM Runtime 原则

1. Runtime 必须定义生命周期。
2. Runtime 必须定义错误处理。
3. Runtime 必须记录审计日志。
4. Runtime 不得隐藏失败路径。

## 8. AOEM GPU 原则

1. GPU 调度必须有资源隔离。
2. GPU 任务必须可追踪。
3. 生产任务和实验任务必须隔离。
4. GPU 优化不得改变业务语义、权限语义和审计语义。

## 9. AOEM Privacy 原则

1. 隐私计算必须遵守数据最小化。
2. 明文边界和密文边界必须清晰。
3. 日志必须默认脱敏。
4. RingCT、Privacy Execute 或其他隐私机制进入主链路前必须完成知识认证。

## 10. AOEM Architecture Decisions

所有 AOEM 重大设计必须进入：

1. `MCP/16_Knowledge_Base/AOEM/10_Architecture_Decisions`
2. `MCP/17_Memory_Center/decision_registry.md`
3. `MCP/17_Memory_Center/architecture_decision_record.md`
