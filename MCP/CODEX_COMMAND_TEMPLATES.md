# Codex Command Templates

本文档定义 OMCF / WPF-MCP V4 的可复用 Codex 命令模板。每个项目只需要替换项目名称、项目类型、项目资料和当前阶段。

## 0. OMCF V4 能力门禁命令

```text
【OMCF V4 能力门禁】

执行原则：

1. 禁止新增角色
2. 禁止预设项目记忆槽位
3. 诸葛亮分配任务前必须查询 Capability Matrix
4. 赵云审计前必须检查 Knowledge Certification
5. AOEM 任务必须遵守 AOEM Constitution
6. 重大选择和拒绝方案必须进入 Decision Registry
7. 能力不足则先训练，不得硬接任务
```

## 1. OMCF V4 项目启动命令

```text
【OMCF V4 启动】

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
4. 仓颉按需创建项目记忆，不得预设无关项目槽位
5. 鬼谷子输出战略影响判断
6. 扁鹊登记新知识吸收和专家训练需求
7. 诸葛亮生成项目计划和任务树
8. 墨子确认架构边界和技术路线
9. 嬴政建立文档体系
10. 如涉及 AOEM、数学模型或新语言，自动引入庞统、华佗、庄周
11. 检查专家成熟度 Level
12. 检查 Capability Matrix
13. 检查 Knowledge Certification
14. AOEM 任务检查 AOEM Constitution
15. 赵云进行阶段审计
16. 审计通过后才允许进入开发阶段
```

## 2. OMCF V4 总命令

```text
【OMCF V4】

既有永久机构：

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
9. 专家成熟度低于 Level 3，不得独立输出生产级方案
10. 每个项目记忆必须按需创建，不得预设项目槽位
11. Capability Matrix 不满足任务要求不得分配任务
12. Knowledge Certification 未认证不得承接生产任务
13. 所有任务必须经过赵云审计
14. 审计失败二次复审，二次复审失败退回重做
```

## 3. WPF-MCP V4 项目命令

```text
【WPF-MCP V4】

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
项目记忆必须在项目正式启动时按需创建。
```

## 4. AOEM 专家任务命令

```text
【调用 庞统 / AOEM-001】

任务名称：
<AOEM 内核、GPU 调度、隐私计算或执行优化任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V3_5_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/13_AOEM/README.md
5. MCP/16_Knowledge_Base/AOEM/README.md
6. MCP/19_Learning_Center/expert_training_register.md
7. MCP/20_Expert_Training/capability_matrix.md
8. MCP/20_Expert_Training/knowledge_certification.md
9. MCP/16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md

输出限制：
如庞统训练状态不是 TRAINED、能力矩阵不满足任务要求或知识认证不是 CERTIFIED，只能输出资料缺口、学习计划、风险提示，不得输出 AOEM 定论。

审计要求：
赵云审计 + 墨子或张飞技术复核 + 伏羲知识来源检查 + AOEM 宪法检查
```

## 5. 数学专家任务命令

```text
【调用 华佗 / MATH-001】

任务名称：
<代数结构、数学证明、量子计算或模型验证任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V3_5_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/14_Math/README.md
5. MCP/16_Knowledge_Base/README.md
6. MCP/19_Learning_Center/expert_training_register.md
7. MCP/20_Expert_Training/capability_matrix.md
8. MCP/20_Expert_Training/knowledge_certification.md

输出限制：
如华佗训练状态不是 TRAINED、能力矩阵不满足任务要求或知识认证不是 CERTIFIED，只能输出假设、待验证问题和验证计划，不得输出数学理论定论。

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
2. MCP/MCP_V3_5_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/15_Language/README.md
5. MCP/16_Knowledge_Base/AOEM/README.md
6. MCP/19_Learning_Center/expert_training_register.md
7. MCP/20_Expert_Training/capability_matrix.md
8. MCP/20_Expert_Training/knowledge_certification.md

输出限制：
如庄周训练状态不是 TRAINED、能力矩阵不满足任务要求或知识认证不是 CERTIFIED，只能输出语言研究计划、语义问题清单和原型边界，不得输出语言设计定论。

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
