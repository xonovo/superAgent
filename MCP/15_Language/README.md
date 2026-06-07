# 15_Language

本目录归属 Language-Codex（庄周 / LANG-001），用于沉淀新语言自动演化、语义模型、指令集设计、编译优化和语言原型相关规范。

## 职责范围

1. 新语言目标、非目标和语义边界。
2. DSL、指令集和运行时交互规则。
3. 自动编译优化和语言自动演化算法。
4. AOEM 指令扩展和 AI Agent 指令抽象。
5. 语言原型验证和 compiler-sanity-test。

## 核心文档

| 文档 | 说明 |
|---|---|
| `language_evolution_spec.md` | 新语言自动演化规范 |
| `instruction_set_design.md` | 指令集设计规范 |
| `compiler_sanity_test.md` | 编译器基础验证规范 |
| `language_task_template.md` | 新语言专项任务模板 |

## 审计要求

1. 新语言方案必须先由墨子审批架构兼容性。
2. 任何编译优化不得改变业务可观察语义。
3. 进入项目主链路前必须通过赵云审计。
4. 影响 AOEM 核心执行时必须引入庞统协作。
