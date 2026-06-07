# superAgent OMCF / WPF-MCP V3

本目录是 superAgent 的 AI 自治研发体系文档中心。

`OMCF` 是 OneMan AI Company Framework，即“一人 AI 公司框架”。V3 在 V2.1 的组织、流程、审计基础上新增 `Memory` 层，使 Codex 角色拥有可追溯、可审计、可复用的知识库和长期记忆。

`MCP` 在本目录中只表示 `Master Control Protocol`，即内部总控协议；它不是 Anthropic 的 `Model Context Protocol`。

## 核心模型

```text
OMCF
├── Core                 永久组织、角色、协作边界
├── Project Pack         项目资料包
├── Delivery             任务、文档、设计、开发、测试、部署
├── Audit                审计门禁、复审、发布阻断
└── Memory               知识库、长期记忆、学习、战略
```

## V3 核心目标

1. 统一组织
2. 统一思想
3. 统一数据
4. 统一规则
5. 统一文档
6. 统一知识
7. 统一记忆
8. 再统一代码

任何专家不得依赖模型自身记忆。所有专业结论必须来自 `Knowledge_Base`，所有历史判断必须来自 `Memory_Center`。

## 总体链路

```text
King Xu
  -> 女娲 / CAIO / AI 总经理
    -> 伏羲 / CKO / 知识中心
    -> 仓颉 / CMO / 记忆中心
    -> 鬼谷子 / CSO / 战略中心
    -> 扁鹊 / CLO / 学习中心
    -> 诸葛亮 / CEO / PM 总控
      -> 墨子 / CTO / 总架构师
        -> 专业 Codex 部门
          -> 赵云 / Auditor Codex / 独立审计
```

## 永久组织

永久组织不随项目变化。未来无论是 WPF、NOVOVM、钱包、官网、AI 产品还是政务项目，都复用同一套组织。

```text
King Xu
│
└── 女娲（CAIO / AI 总经理）
     │
     ├── 伏羲（CKO-001 / 知识总监）
     ├── 仓颉（CMO-001 / 记忆总监）
     ├── 鬼谷子（CSO-001 / 战略总监）
     ├── 扁鹊（CLO-001 / 学习总监）
     │
     ├── 诸葛亮（PM-001 / CEO / 项目总经理）
     ├── 墨子（ARC-001 / CTO / 总架构师）
     ├── 嬴政（DOC-001 / CAO / 文档行政中心）
     │
     ├── 鲁班七号（DB-001 / 数据库总监）
     ├── 项羽（DATA-001 / 数据治理总监）
     ├── 司马懿（BE-001 / 后端研发总监）
     ├── 妲己（FE-001 / 前端研发总监）
     ├── 孙尚香（MOB-001 / 移动端研发总监）
     ├── 貂蝉（UI-001 / 设计总监）
     ├── 刘备（API-001 / 生态接口总监）
     ├── 张飞（OPS-001 / 基础设施总监）
     ├── 王昭君（AI-001 / AI 研发总监）
     ├── 庞统（AOEM-001 / AOEM 内核专家）
     ├── 华佗（MATH-001 / 数学建模专家）
     ├── 庄周（LANG-001 / 新语言演化专家）
     │
     └── 赵云（AUD-001 / 首席审计官）
```

## 目录说明

```text
MCP/
├── 00_Project_Charter      项目章程、治理边界、决策权限
├── 01_Product              产品定义、PRD、用户角色、业务流程
├── 02_Architecture         技术架构、模块拆分、系统边界
├── 03_Database             数据模型、迁移策略、数据字典
├── 04_API                  接口规范、外部系统集成、鉴权约定
├── 05_UI                   UI 规范、设计系统、页面标准
├── 06_AI                   AI 模型、数据蒸馏、画像体系
├── 07_Server               服务器、Linux、Docker、K8S、GPU 集群
├── 08_Test                 测试策略、测试用例、验收标准
├── 09_Audit                数据审计、代码审计、安全审计、发布审计
├── 10_Deployment           发布流程、回滚方案、环境规则
├── 11_Document             文档体系、汇报材料、招投标材料
├── 12_Data_Governance      数据治理、质量检查、训练数据准备
├── 13_AOEM                 AOEM 内核、GPU 调度、隐私计算、执行优化
├── 14_Math                 代数结构、数理验证、量子计算、模型证明
├── 15_Language             新语言语义、指令集设计、编译优化、自动演化
├── 16_Knowledge_Base       AOEM、NOVOVM、物业、法规、项目知识库
├── 17_Memory_Center        项目历史、决策记录、架构记录、失败经验
├── 18_Strategy_Center      商业分析、产品路线、竞争分析、长期规划
└── 19_Learning_Center      新文档吸收、知识蒸馏、训练集、专家成长
```

## 工作原则

任何专业 Codex 在执行任务前必须先读取：

1. `MCP/README.md`
2. `MCP/MCP_V3_MASTER_CONTROL_PROTOCOL.md`
3. `MCP/AGENT_ROLE_MATRIX.md`
4. `MCP/CODEX_COMMAND_TEMPLATES.md`
5. 与任务相关领域目录下的 `README.md`
6. `MCP/16_Knowledge_Base/README.md`
7. `MCP/17_Memory_Center/README.md`
8. 当前任务卡和审计清单

没有知识库依据、没有记忆检索、没有文档依据的实现，不进入发布流程。

## 专家训练红线

以下规则为 V3 强制门禁：

1. 未经知识库训练完成，庞统不得输出 AOEM 结论。
2. 未经知识库训练完成，华佗不得输出数学理论结论。
3. 未经知识库训练完成，庄周不得输出语言设计结论。
4. 新资料必须进入 `Learning_Center`，再进入 `Knowledge_Base`。
5. 历史决策必须进入 `Memory_Center`。
6. 战略规划必须进入 `Strategy_Center`。

## 人工确认红线

以下事项必须由 King Xu 人工确认后才能执行：

1. 历史数据库结构变更
2. 历史系统覆盖、替换或不可逆迁移
3. 银行、支付、产权登记、资金接口变更
4. AI 训练数据、蒸馏数据、自动决策规则变更
5. AOEM 核心执行逻辑、隐私计算逻辑、GPU 调度策略变更
6. 新语言语义、指令集、编译器行为进入项目主链路
7. 生产环境发布、回滚、权限升级
