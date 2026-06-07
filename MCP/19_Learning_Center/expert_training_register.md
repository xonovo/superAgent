# Expert Training Register

## 状态定义

- `UNTRAINED`：未训练，不得输出专业结论。
- `LEARNING`：学习中，只能输出资料缺口和学习计划。
- `REVIEW_READY`：待复核，可输出假设和验证计划。
- `TRAINED`：已训练，可在知识库范围内输出专业结论。
- `EXPIRED`：知识过期，必须重新训练。

## 专家训练状态

| 专家 | 代号 | 领域 | 当前状态 | 成熟度 | 知识认证 | 必须知识库 | 最近训练记录 | 输出限制 |
|---|---|---|---|---|---|---|---|---|
| 庞统 | AOEM-001 | AOEM 内核 | UNTRAINED | Level 0 | UNCERTIFIED | `MCP/16_Knowledge_Base/AOEM` | 待填写 | 不得输出 AOEM 定论 |
| 华佗 | MATH-001 | 代数语义与数学模型 | UNTRAINED | Level 0 | UNCERTIFIED | `MCP/16_Knowledge_Base/AOEM`、`MCP/14_Math` | 待填写 | 不得输出数学理论定论 |
| 庄周 | LANG-001 | 新语言与指令集 | UNTRAINED | Level 0 | UNCERTIFIED | `MCP/16_Knowledge_Base/AOEM`、`MCP/15_Language` | 待填写 | 不得输出语言设计定论 |

## V3.5 成熟度说明

成熟度等级以 `MCP/20_Expert_Training/expert_maturity_model.md` 为准。训练状态表示是否完成训练流程，成熟度表示专家能独立承担的能力边界。

## V4 能力门禁

- 能力矩阵：`MCP/20_Expert_Training/capability_matrix.md`
- 知识认证：`MCP/20_Expert_Training/knowledge_certification.md`
- AOEM 宪法：`MCP/16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md`
- 决策注册：`MCP/17_Memory_Center/decision_registry.md`
