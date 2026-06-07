# Codex Command Templates

本文档定义 OMCF / WPF-MCP V2.1 的可复用 Codex 命令模板。每个项目只需要替换项目名称、项目类型、项目资料和当前阶段。

## 1. OMCF 项目启动命令

```text
【OMCF V2.1 启动】

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
2. 诸葛亮生成项目计划和任务树
3. 墨子确认架构边界和技术路线
4. 嬴政建立文档体系
5. 各专业 Codex 只输出设计，不直接编码
6. 如涉及 AOEM、数学模型或新语言，自动引入庞统、华佗、庄周
7. 赵云进行阶段审计
8. 审计通过后才允许进入开发阶段
```

## 2. WPF-MCP V2.1 项目命令

```text
【WPF-MCP V2.1】

角色冻结：

女娲（CAIO）
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

执行原则：

1. 历史数据库不得删除
2. 历史系统不得直接覆盖
3. 先文档后开发
4. 先设计后编码
5. 所有任务必须经过赵云审计
6. 审计失败二次复审
7. 二次复审失败退回重做
8. 涉及数据结构变更必须人工确认
9. 涉及银行接口变更必须人工确认
10. 涉及 AI 训练数据变更必须人工确认
11. 涉及 AOEM 核心执行逻辑必须人工确认
12. 涉及数学模型进入生产判断链路必须人工确认
13. 涉及新语言主链路落地必须人工确认

当前进入：

Phase-1 文档建设阶段

禁止直接编码
```

## 3. AOEM 专家任务命令

```text
【调用 庞统 / AOEM-001】

任务名称：
<AOEM 内核、GPU 调度、隐私计算或执行优化任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V2_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/13_AOEM/README.md
5. MCP/13_AOEM/aoem_core_spec.md

输出要求：
1. 说明 AOEM 能力边界
2. 说明核心执行逻辑
3. 说明 GPU/隐私计算调度策略
4. 给出验证方法
5. 标记是否需要 King Xu 人工确认

审计要求：
赵云审计 + 墨子或张飞技术复核
```

## 4. 数学专家任务命令

```text
【调用 华佗 / MATH-001】

任务名称：
<代数结构、数学证明、量子计算或模型验证任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V2_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/14_Math/README.md
5. MCP/14_Math/algebra_spec.md

输出要求：
1. 定义数学对象和符号
2. 列出假设和适用边界
3. 给出推导或证明草案
4. 给出验证方法和误差边界
5. 标记是否需要二次确认

审计要求：
赵云审计 + 数学模型二次确认
```

## 5. 新语言专家任务命令

```text
【调用 庄周 / LANG-001】

任务名称：
<新语言语义、指令集、编译优化或语言原型任务>

必须读取：
1. MCP/README.md
2. MCP/MCP_V2_MASTER_CONTROL_PROTOCOL.md
3. MCP/AGENT_ROLE_MATRIX.md
4. MCP/15_Language/README.md
5. MCP/15_Language/language_evolution_spec.md

输出要求：
1. 定义语言目标和非目标
2. 定义语义模型和指令集边界
3. 说明编译优化规则
4. 给出 compiler-sanity-test
5. 标记是否需要进入项目主链路

审计要求：
赵云审计 + 墨子架构审批
```

## 6. 审计命令

```text
【调用 赵云 / AUD-001】

审计对象：
<任务编号或输出物路径>

审计类型：
<文档 / 代码 / 数据 / 安全 / AI / AOEM / 数学模型 / 新语言 / 发布>

必须读取：
1. 任务卡
2. 输入文档
3. 输出物
4. MCP/AUDIT_GATE_RULES.md
5. 对应领域 README

输出要求：
1. PASS 或 FAIL
2. 证据清单
3. 风险等级
4. 整改建议
5. 是否进入二次复审
6. 是否需要 King Xu 人工确认
```
