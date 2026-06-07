# 20_Expert_Training

本目录归属扁鹊（CLO-001 / Chief Learning Officer），用于执行专家训练、专家成熟度评估和能力升级。

## 定位

V3.5 不再继续增加角色，而是让已有专家真正成长。专家能力由文档、知识库、训练记录、任务表现和审计结果共同决定。

## 核心机制

```text
知识进入
  -> 知识整理
    -> 知识训练
      -> 专家成长
        -> 项目应用
          -> 经验沉淀
            -> 回流知识库
```

## 核心文档

| 文档 | 说明 |
|---|---|
| `expert_maturity_model.md` | 专家成熟度 Level 0-5 |
| `capability_matrix.md` | 能力矩阵 |
| `knowledge_certification.md` | 知识认证 |
| `knowledge_flywheel.md` | 知识飞轮与经验回流 |
| `training_task_template.md` | 专家训练任务模板 |
| `maturity_assessment.md` | 专家成熟度评估记录 |

## 专家目录

| 专家 | 目录 | 训练目标 |
|---|---|---|
| 庞统 / AOEM-001 | `PangTong` | AOEM 内核、Runtime、GPU、Privacy、SDK |
| 华佗 / MATH-001 | `HuaTuo` | 代数语义、数学推导、模型设计、新理论 |
| 庄周 / LANG-001 | `ZhuangZhou` | AOEM 语义、DSL、编译器、新计算语言 |

## 强制规则

1. 专家成熟度低于 Level 3，不得独立输出生产级方案。
2. 专家成熟度低于 Level 4，不得独立优化核心系统。
3. 专家成熟度低于 Level 5，不得设计新能力、新理论或新计算语言。
4. 成熟度升级必须有训练证据、项目应用证据和赵云审计记录。
5. 能力矩阵不满足任务要求时不得分配任务。
6. 知识认证未通过时不得承接对应生产任务。
