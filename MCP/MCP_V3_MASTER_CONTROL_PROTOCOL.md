# OMCF V3 Master Control Protocol

## 1. 定位

OMCF V3 是 superAgent 的 AI Company Operating System。它在 V2.1 的组织、流程和审计基础上，新增 `Memory` 层，让 Codex 角色不再依赖模型自身记忆，而是依赖可追溯、可审计、可复用的知识库和长期记忆。

`MCP` 在本文档中表示 `Master Control Protocol`，不表示 Anthropic 的 `Model Context Protocol`。

## 2. V3 复用模型

```text
OMCF
├── Core                 永久组织、角色、协作边界
├── Project Pack         项目资料包
├── Delivery             任务、文档、设计、开发、测试、部署
├── Audit                审计门禁、复审、发布阻断
└── Memory               知识库、长期记忆、学习、战略
```

V3 的核心升级是：

1. 所有专业知识必须来源于 `Knowledge_Base`。
2. 所有历史决策必须来源于 `Memory_Center`。
3. 所有战略规划必须记录进入 `Strategy_Center`。
4. 所有新知识必须进入 `Learning_Center`。
5. 任何专家不得依赖模型自身记忆输出专业结论。

## 3. 管理链路

```text
King Xu
  -> 女娲 / CAIO
    -> 伏羲 / CKO / 知识中心
    -> 仓颉 / CMO / 记忆中心
    -> 鬼谷子 / CSO / 战略中心
    -> 扁鹊 / CLO / 学习中心
    -> 诸葛亮 / PM-001
      -> 墨子 / ARC-001
        -> 专业 Codex Agent
          -> 赵云 / AUD-001
```

## 4. 新增永久机构

| 机构 | 角色 | 代号 | 昵称 | 核心职责 | 归档目录 |
|---|---|---|---|---|---|
| 知识中心 | Chief Knowledge Officer | CKO-001 | 伏羲 | 管理 AOEM、NOVOVM、物业、法规、项目知识库 | `MCP/16_Knowledge_Base` |
| 记忆中心 | Chief Memory Officer | CMO-001 | 仓颉 | 管理项目历史、决策记录、架构记录、失败经验 | `MCP/17_Memory_Center` |
| 战略中心 | Chief Strategy Officer | CSO-001 | 鬼谷子 | 商业分析、产品路线、竞争分析、长期规划 | `MCP/18_Strategy_Center` |
| 学习中心 | Chief Learning Officer | CLO-001 | 扁鹊 | 新文档吸收、知识蒸馏、训练集整理、专家成长 | `MCP/19_Learning_Center` |

## 5. V3 强制原则

1. 未经知识库训练完成，庞统不得输出 AOEM 结论。
2. 未经知识库训练完成，华佗不得输出数学理论结论。
3. 未经知识库训练完成，庄周不得输出语言设计结论。
4. 任何项目开始前必须读取对应 `Project Pack`、`Knowledge_Base` 和 `Memory_Center`。
5. 任何架构决策必须记录进入 `Architecture_Decision_Record`。
6. 任何失败、返工、审计不通过必须记录进入 `Failure_Lessons`。
7. 任何战略判断必须记录进入 `Strategy_Center`。
8. 任何外部资料进入 OMCF 前必须由扁鹊完成吸收、摘要、标签和来源登记。

## 6. 专家训练门禁

### 庞统 / AOEM-001

庞统输出 AOEM 专业结论前，必须引用：

1. `MCP/16_Knowledge_Base/AOEM/AOEM_Theory`
2. `MCP/16_Knowledge_Base/AOEM/AOEM_Runtime`
3. `MCP/16_Knowledge_Base/AOEM/AOEM_GPU`
4. `MCP/16_Knowledge_Base/AOEM/AOEM_Privacy`
5. `MCP/19_Learning_Center/expert_training_register.md`

如果训练状态不是 `TRAINED`，只能输出问题清单、学习计划和资料缺口，不得输出定论。

### 华佗 / MATH-001

华佗输出数学理论结论前，必须引用：

1. `MCP/16_Knowledge_Base/AOEM/AOEM_Theory`
2. `MCP/14_Math/algebra_spec.md`
3. `MCP/14_Math/math_model_validation.md`
4. `MCP/19_Learning_Center/expert_training_register.md`

如果训练状态不是 `TRAINED`，只能输出假设、待验证问题和验证计划，不得输出定论。

### 庄周 / LANG-001

庄周输出语言设计结论前，必须引用：

1. `MCP/16_Knowledge_Base/AOEM/AOEM_Theory`
2. `MCP/15_Language/language_evolution_spec.md`
3. `MCP/15_Language/instruction_set_design.md`
4. `MCP/19_Learning_Center/expert_training_register.md`

如果训练状态不是 `TRAINED`，只能输出语言研究计划、语义问题清单和原型边界，不得输出定论。

## 7. 任务生命周期

```text
需求进入
  -> 仓颉检索历史记忆
  -> 伏羲检索知识库
  -> 鬼谷子判断战略影响
  -> 扁鹊登记新知识吸收需求
  -> 诸葛亮生成任务
  -> 墨子确认架构边界
  -> 专业 Codex 执行
  -> 赵云审计
  -> 仓颉记录决策、失败或发布记忆
```

## 8. 任务卡新增必填项

V3 任务卡除 V2.1 字段外，必须新增：

1. 知识库引用。
2. 历史记忆引用。
3. 战略影响记录。
4. 新知识吸收记录。
5. 专家训练状态。
6. 决策记录编号。
7. 失败经验记录编号。

## 9. 审计门禁新增项

赵云审计时必须检查：

1. 专业结论是否有知识库来源。
2. 历史决策是否已检索。
3. 新知识是否已进入学习中心。
4. 专家训练状态是否允许输出结论。
5. 架构和战略决策是否已归档。
6. 失败经验是否已记录。

## 10. 当前版本

当前版本：`V3.0-DRAFT`
