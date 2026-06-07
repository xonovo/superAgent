# OMCF V3.5 Master Control Protocol

## 1. 定位

OMCF V3.5 是 V3 Memory System 的能力增长版本。V3 解决“有知识、有记忆”的问题，V3.5 解决“知识如何变成专家能力，项目经验如何回流成组织能力”的问题。

V3.5 不新增角色，只新增机制：

1. Expert Maturity：专家成熟度。
2. Knowledge Flywheel：知识飞轮。
3. Project Memory：项目级记忆。
4. Experience Feedback：经验回流。

## 2. V3.5 核心闭环

```text
知识进入
  -> 知识整理
    -> 知识训练
      -> 专家成长
        -> 项目应用
          -> 经验沉淀
            -> 回流知识库
```

## 3. 新增能力层

| 能力 | 目录 | 责任角色 | 目标 |
|---|---|---|---|
| 专家训练 | `MCP/20_Expert_Training` | 扁鹊 | 将专家从角色名称训练为可审计能力 |
| 项目记忆 | `MCP/17_Memory_Center/Project_Memory` | 仓颉 | 避免每个项目重新开始 |
| 知识飞轮 | `MCP/20_Expert_Training/knowledge_flywheel.md` | 扁鹊、伏羲、仓颉 | 让项目经验回流知识库 |
| AOEM 知识地图 | `MCP/16_Knowledge_Base/AOEM/AOEM_Knowledge_Map.md` | 伏羲、庞统 | 统一 AOEM 训练入口 |

## 4. 专家成熟度

| Level | 名称 | 能力边界 |
|---|---|---|
| Level 0 | 未训练 | 只能提出资料缺口 |
| Level 1 | 了解文档 | 能复述基础资料 |
| Level 2 | 理解机制 | 能解释机制和边界 |
| Level 3 | 能独立开发 | 能在既有规范内实现 |
| Level 4 | 能独立优化 | 能发现瓶颈并优化 |
| Level 5 | 能设计新能力 | 能提出新架构、新理论、新语言 |

## 5. 三位专家训练路线

### 庞统 / AOEM-001

```text
Level 0  未训练
Level 1  了解 AOEM 文档
Level 2  理解 AOEM Runtime、State、Execution
Level 3  能独立开发 AOEM 扩展
Level 4  能独立优化 AOEM Runtime、GPU、Privacy
Level 5  能设计 AOEM 新能力
```

### 华佗 / MATH-001

```text
Level 0  未训练
Level 1  掌握基础资料
Level 2  理解代数语义
Level 3  能够完成推导和验证
Level 4  能够设计数学模型
Level 5  能够提出新理论
```

### 庄周 / LANG-001

```text
Level 0  未训练
Level 1  理解 AOEM 语义
Level 2  理解语言设计
Level 3  能设计 DSL
Level 4  能设计编译器
Level 5  能设计新计算语言
```

## 6. V3.5 强制原则

1. 专家成熟度低于 Level 3，不得独立输出生产级方案。
2. 专家成熟度低于 Level 4，不得独立优化核心系统。
3. 专家成熟度低于 Level 5，不得设计新能力、新理论或新计算语言。
4. 每个正式启动的项目必须有项目级记忆。
5. 每次审计失败必须进入 Failure Log。
6. 每次发布完成必须进入 Lessons Learned。
7. 可复用经验必须回流 `Knowledge_Base`。
8. 专家升级必须有训练证据、项目证据和审计证据。
9. 不得提前创建未正式启动的项目记忆槽位。

## 7. 当前版本

当前版本：`V3.5-DRAFT`
