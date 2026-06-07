# Codex Command Templates

本文档定义 OMCF / WPF-MCP V3 的可复用 Codex 命令模板。每个项目只需要替换项目名称、项目类型、项目资料和当前阶段。

## 1. OMCF V3 项目启动命令

```text
【OMCF V3 启动】

项目名称：
<Project Name>

项目类型：
<政务 / Web3 / AI产品 / 官网 / 钱包 / 数据平台 / 其他>

当前阶段：
Phase-1 文档建设

项目资料：
<资料路径或资料说明>

资料包模板：
MCP/PROJECT_PACK_TEMPLATE.md

执行要求：
1. 启动女娲总控
2. 伏羲检索项目相关知识库
3. 仓颉检索历史项目、历史决策、历史架构记录
4. 鬼谷子输出战略影响判断
5. 扁鹊登记新知识吸收和专家训练需求
6. 诸葛亮生成项目计划和任务树
7. 墨子确认架构边界和技术路线
8. 嬴政建立文档体系
9. 如涉及 AOEM、数学模型或新语言，自动引入庞统、华佗、庄周
10. 赵云进行阶段审计
11. 审计通过后才允许进入开发阶段
```

## 2. OMCF V3 总命令

```text
【OMCF V3】

新增永久机构：

伏羲（知识中心）
鬼谷子（战略中心）
扁鹊（学习中心）
仓颉（记忆中心）

执行原则：

1. 任何专家不得依赖模型自身记忆
2. 所有专业知识必须来源于 Knowledge_Base
3. 所有历史决策必须来源于 Memory_Center
4. 所有战略规划必须记录进入 Strategy_Center
5. 所有新知识必须进入 Learning_Center
6. 未经知识库训练完成，庞统不得输出 AOEM 结论
7. 未经知识库训练完成，华佗不得输出数学理论结论
8. 未经知识库训练完成，庄周不得输出语言设计结论
9. 所有任务必须经过赵云审计
10. 审计失败二次复审，二次复审失败退回重做
```

## 3. WPF-MCP V3 项目命令

```text
【WPF-MCP V3】

角色冻结：

女娲（CAIO）
伏羲（知识）
仓颉（记忆）
鬼谷子（战略）
扁鹊（学习）
诸葛亮（PM）
墨子（架构）
鲁班七号（数据库）
司马懿（后端）
妲己（前端）
孙尚香（移动端）
貂蝉（UI）
刘备（接口）
张飞（运维）
王昭君（AI）
项羽（数据治理）
嬴政（文档）
庞统（AOEM）
华佗（数学）
庄周（新语言）
赵云（审计）

当前进入：

Phase-1 文档建设阶段

禁止直接编码。
必须先建立知识库、记忆中心、学习中心和专家训练登记。
```

## 4. AOEM 专家任务命令

```text
【调用 庞统 / AOEM-001】

任务名称：
<AOEM 内核、GPU 调度、隐私计算或执行优化任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V3_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/13_AOEM/README.md
5. MCP/16_Knowledge_Base/AOEM/README.md
6. MCP/19_Learning_Center/expert_training_register.md

输出限制：
如庞统训练状态不是 TRAINED，只能输出资料缺口、学习计划、风险提示，不得输出 AOEM 定论。

审计要求：
赵云审计 + 墨子或张飞技术复核 + 伏羲知识来源检查
```

## 5. 数学专家任务命令

```text
【调用 华佗 / MATH-001】

任务名称：
<代数结构、数学证明、量子计算或模型验证任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V3_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/14_Math/README.md
5. MCP/16_Knowledge_Base/README.md
6. MCP/19_Learning_Center/expert_training_register.md

输出限制：
如华佗训练状态不是 TRAINED，只能输出假设、待验证问题和验证计划，不得输出数学理论定论。

审计要求：
赵云审计 + 数学模型二次确认 + 伏羲知识来源检查
```

## 6. 新语言专家任务命令

```text
【调用 庄周 / LANG-001】

任务名称：
<新语言语义、指令集、编译优化或语言原型任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V3_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/15_Language/README.md
5. MCP/16_Knowledge_Base/AOEM/README.md
6. MCP/19_Learning_Center/expert_training_register.md

输出限制：
如庄周训练状态不是 TRAINED，只能输出语言研究计划、语义问题清单和原型边界，不得输出语言设计定论。

审计要求：
赵云审计 + 墨子架构审批 + 伏羲知识来源检查
```

## 7. 记忆检索命令

```text
【调用 仓颉 / CMO-001】

检索对象：
<项目 / 架构 / 决策 / 失败经验 / 发布记录>

必须读取：
1. MCP/17_Memory_Center/README.md
2. MCP/17_Memory_Center/decision_log.md
3. MCP/17_Memory_Center/architecture_decision_record.md
4. MCP/17_Memory_Center/failure_lessons.md

输出要求：
1. 相关历史记录
2. 可复用经验
3. 风险提醒
4. 是否需要新记忆归档
```

## 8. 审计命令

```text
【调用 赵云 / AUD-001】

审计对象：
<任务编号或输出物路径>

审计类型：
<文档 / 代码 / 数据 / 安全 / AI / AOEM / 数学模型 / 新语言 / 记忆 / 知识 / 发布>

必须读取：
1. 任务卡
2. 输入文档
3. 输出物
4. MCP/AUDIT_GATE_RULES.md
5. 对应领域 README
6. 知识库引用
7. 记忆中心引用
8. 专家训练状态

输出要求：
1. PASS 或 FAIL
2. 证据清单
3. 风险等级
4. 整改建议
5. 是否进入二次复审
6. 是否需要 King Xu 人工确认
```
