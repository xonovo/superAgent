# Capability Matrix

## 1. 定位

Capability Matrix 是 OMCF V4 的任务分配门禁。诸葛亮分派任务前，必须先检查责任角色是否具备对应能力等级和知识认证。

V4 不新增角色。V4 只让已有角色的能力边界变得可查询、可审计、可升级。

## 2. 能力等级

| Level | 名称 | 能力边界 |
|---|---|---|
| Level 0 | 未训练 | 只能提出资料缺口 |
| Level 1 | 了解文档 | 能复述基础资料 |
| Level 2 | 理解机制 | 能解释机制和边界 |
| Level 3 | 能独立开发 | 能在既有规范内实现 |
| Level 4 | 能独立优化 | 能发现瓶颈并优化 |
| Level 5 | 能设计新能力 | 能提出新架构、新理论、新语言 |

## 3. 庞统能力矩阵

| 能力域 | Level | 知识认证 | 允许任务 | 禁止任务 |
|---|---|---|---|---|
| AOEM_Theory | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | AOEM 理论定论 |
| AOEM_Runtime | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | Runtime 设计 |
| AOEM_GPU | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | GPU 调度方案 |
| AOEM_Privacy | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 隐私计算方案 |
| AOEM_SDK | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | SDK 设计 |

## 4. 华佗能力矩阵

| 能力域 | Level | 知识认证 | 允许任务 | 禁止任务 |
|---|---|---|---|---|
| 代数结构 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 数学定论 |
| 代数语义 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 语义证明 |
| 量子计算 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 量子算法方案 |
| 索尔算法 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 算法定论 |

## 5. 庄周能力矩阵

| 能力域 | Level | 知识认证 | 允许任务 | 禁止任务 |
|---|---|---|---|---|
| 语言设计 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 语言设计定论 |
| 编译原理 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | 编译器方案 |
| AOEM 语义 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | AOEM 语言绑定 |
| DSL 设计 | Level 0 | UNCERTIFIED | 资料缺口、学习计划 | DSL 主链路方案 |

## 6. 任务分配规则

1. 任务要求 Level 3 时，专家能力必须达到 Level 3 且知识认证为 `CERTIFIED`。
2. 任务要求 Level 4 时，专家能力必须达到 Level 4 且知识认证为 `CERTIFIED`。
3. 任务要求 Level 5 时，专家能力必须达到 Level 5、知识认证为 `CERTIFIED`，并由 King Xu 或女娲确认。
4. 能力 Level 足够但知识未认证时，不得接任务。
5. 知识认证通过但 Level 不足时，不得接超边界任务。

## 7. 更新规则

能力矩阵只能由扁鹊维护，赵云审计，女娲确认。任何项目任务不得直接修改能力矩阵。
