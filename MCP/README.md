# superAgent OMCF / WPF-MCP V4

本目录是 superAgent 的 AI 自治研发体系文档中心。

`OMCF` 是 OneMan AI Company Framework，即“一人 AI 公司框架”。V3 建立知识库和长期记忆，V3.5 建立专家成熟度、知识飞轮、项目记忆和经验回流。V4 不新增角色、不新增顶层目录，而是新增能力矩阵、知识认证、AOEM 宪法和决策注册表，让任务分配从“按角色”升级为“按能力和认证”。

`MCP` 在本目录中只表示 `Master Control Protocol`，即内部总控协议；它不是 Anthropic 的 `Model Context Protocol`。

## 核心模型

```text
OMCF
├── Core                 永久组织、角色、协作边界
├── Project Pack         项目资料包
├── Delivery             任务、文档、设计、开发、测试、部署
├── Audit                审计门禁、复审、发布阻断
├── Memory               知识库、长期记忆、学习、战略
└── Capability           能力矩阵、知识认证、宪法约束、决策注册
```

## V4 核心闭环

```text
知识进入
  -> 知识整理
    -> 知识训练
      -> 专家成长
        -> 项目应用
          -> 经验沉淀
            -> 回流知识库
              -> 更新能力矩阵
                -> 更新知识认证
```

## 总体链路

```text
King Xu
  -> 女娲 / CAIO / AI 总经理
    -> 伏羲 / CKO / 知识中心
    -> 仓颉 / CMO / 记忆中心
    -> 鬼谷子 / CSO / 战略中心
    -> 扁鹊 / CLO / 学习与训练中心
    -> 诸葛亮 / CEO / PM 总控
      -> 墨子 / CTO / 总架构师
        -> 专业 Codex 部门
          -> 赵云 / Auditor Codex / 独立审计
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
├── 17_Memory_Center        全局记忆与项目级记忆
├── 18_Strategy_Center      商业分析、产品路线、竞争分析、长期规划
├── 19_Learning_Center      新文档吸收、知识蒸馏、训练集、专家成长
└── 20_Expert_Training      专家成熟度、训练路线、知识飞轮
```

## 工作原则

任何专业 Codex 在执行任务前必须先读取：

1. `MCP/README.md`
2. `MCP/MCP_V3_5_MASTER_CONTROL_PROTOCOL.md`
3. `MCP/AGENT_ROLE_MATRIX.md`
4. `MCP/CODEX_COMMAND_TEMPLATES.md`
5. 与任务相关领域目录下的 `README.md`
6. `MCP/16_Knowledge_Base/README.md`
7. `MCP/17_Memory_Center/README.md`
8. `MCP/20_Expert_Training/expert_maturity_model.md`
9. `MCP/20_Expert_Training/capability_matrix.md`
10. `MCP/20_Expert_Training/knowledge_certification.md`
11. 当前任务卡和审计清单

V4 不新增协议文件；V4 使用 `MCP_V3_5_MASTER_CONTROL_PROTOCOL.md` 作为组织与记忆基础，并用能力矩阵、知识认证、AOEM 宪法和决策注册表作为新增执行门禁。

没有知识库依据、没有项目记忆检索、没有专家成熟度依据的专业结论，不进入发布流程。

## V4 强制门禁

1. 专家成熟度低于 Level 3，不得独立输出生产级方案。
2. 专家成熟度低于 Level 4，不得独立优化核心系统。
3. 专家成熟度低于 Level 5，不得设计新能力、新理论或新计算语言。
4. Capability Matrix 不满足任务要求，不得分配任务。
5. Knowledge Certification 未认证，不得承接对应生产任务。
6. AOEM 任务不得违反 AOEM Constitution。
7. 重大选择和拒绝方案必须进入 Decision Registry。
8. 每个正式启动的项目必须有项目级记忆。
9. 审计失败必须进入 Failure Log。
10. 发布完成必须进入 Lessons Learned。
11. 可复用经验必须回流 `Knowledge_Base`。

## 人工确认红线

以下事项必须由 King Xu 人工确认后才能执行：

1. 历史数据库结构变更
2. 历史系统覆盖、替换或不可逆迁移
3. 银行、支付、产权登记、资金接口变更
4. AI 训练数据、蒸馏数据、自动决策规则变更
5. AOEM 核心执行逻辑、隐私计算逻辑、GPU 调度策略变更
6. 新语言语义、指令集、编译器行为进入项目主链路
7. 生产环境发布、回滚、权限升级
