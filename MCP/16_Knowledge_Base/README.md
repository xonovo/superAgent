# 16_Knowledge_Base

本目录归属伏羲（CKO-001 / Chief Knowledge Officer），用于管理 OMCF 的永久知识资产。

## 定位

Knowledge Base 是所有 Codex 专业结论的来源。任何专家不得依赖模型自身记忆输出专业结论。

## 知识域

| 知识域 | 目录 | 责任角色 |
|---|---|---|
| AOEM 知识库 | `AOEM` | 伏羲、庞统、扁鹊 |
| NOVOVM 知识库 | `NOVOVM` | 伏羲、鬼谷子、墨子 |
| 物业知识库 | `Property` | 伏羲、诸葛亮、项羽 |
| 法规知识库 | `Regulation` | 伏羲、赵云、嬴政 |
| 项目知识库 | `Project` | 伏羲、仓颉、嬴政 |

## 知识入库要求

每条知识必须包含：

1. 来源。
2. 摘要。
3. 适用范围。
4. 不适用范围。
5. 关联项目。
6. 关联角色。
7. 更新时间。
8. 可信等级。

## 可信等级

- `L0_RAW`：原始资料，尚未整理。
- `L1_SUMMARIZED`：已摘要。
- `L2_STRUCTURED`：已结构化。
- `L3_REVIEWED`：已复核。
- `L4_ACTIVE`：允许作为任务依据。

## 强制规则

1. `L0_RAW` 和 `L1_SUMMARIZED` 不得作为最终专业结论依据。
2. AOEM、数学、新语言任务必须引用 `L3_REVIEWED` 以上知识。
3. 生产相关任务必须引用 `L4_ACTIVE` 知识。
