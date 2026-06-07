# Decision Registry

## 1. 定位

Decision Registry 是 OMCF V4 的决策注册表，用于记录为什么选择某方案、为什么拒绝某方案，以及该决策影响哪些项目、知识库和专家训练。

Decision Registry 不替代 ADR。ADR 记录架构决策细节，Decision Registry 提供全局可检索索引。

## 2. 决策类型

| 类型 | 说明 |
|---|---|
| ARCHITECTURE | 架构决策 |
| KNOWLEDGE | 知识体系决策 |
| CAPABILITY | 能力矩阵决策 |
| CERTIFICATION | 知识认证决策 |
| PROJECT | 项目级决策 |
| REJECTION | 被拒绝方案 |

## 3. 决策注册表

| Decision ID | 日期 | 类型 | 决策主题 | 选择方案 | 拒绝方案 | 原因 | 影响范围 | 关联 ADR | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| DEC-V4-0001 | 待填写 | CAPABILITY | V4 不新增角色，新增能力矩阵 | Capability Matrix | 继续增加角色 | 角色已足够，瓶颈在能力调度 | OMCF 全局 | 待填写 | DRAFT |
| DEC-V4-0002 | 待填写 | KNOWLEDGE | AOEM 先建立宪法再扩展知识 | AOEM Constitution | 直接堆资料 | 防止知识漂移 | AOEM 知识库 | 待填写 | DRAFT |
| DEC-V4-0003 | 待填写 | PROJECT | Project Memory 按需创建 | 模板化按需创建 | 预设项目槽位 | 防止空项目和知识污染 | 所有项目 | 待填写 | DRAFT |
| DEC-RUNTIME-0001 | 2026-06-07 | ARCHITECTURE | Freeze OMCF Runtime V2.6 and stop version-chasing | V2.6 as Control Plane baseline | Continue V2.7/V2.8 before production | Real execution is more valuable than more control-plane design | OMCF Runtime, Providers, Production Runs | ADR-0002 | ACCEPTED |
| DEC-PROD-0001 | 2026-06-07 | PROJECT | Start real project memory for Zhuzhou Property Supervision Platform | Create Zhuzhou_Property_Platform memory because project is explicitly started | Keep all production artifacts only in ignored runtime runs | Production execution needs auditable committed memory | Zhuzhou Property Supervision Platform | ADR-0002 | ACCEPTED |

## 4. 强制规则

1. 重大架构选择必须进入 Decision Registry。
2. 被拒绝方案必须记录原因。
3. AOEM Constitution 修改必须登记。
4. Capability Matrix 修改必须登记。
5. Knowledge Certification 状态变化必须登记。
