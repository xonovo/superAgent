# Knowledge Certification

## 1. 定位

Knowledge Certification 是 OMCF V4 的知识认证门禁。专家成熟度说明专家能做什么，知识认证说明专家是否已经被验证可以在某个知识域输出结论。

## 2. 认证状态

| 状态 | 含义 | 是否允许接任务 |
|---|---|---|
| UNCERTIFIED | 未认证 | 否 |
| CANDIDATE | 候选认证 | 仅允许学习和验证任务 |
| CERTIFIED | 已认证 | 是，受 Level 限制 |
| SUSPENDED | 暂停认证 | 否 |
| EXPIRED | 认证过期 | 否，必须复训 |

## 3. 认证要求

每个知识域认证必须具备：

1. 知识库来源。
2. 学习记录。
3. 训练任务。
4. 案例分析。
5. 审计结果。
6. 认证结论。
7. 有效期。

## 4. 认证登记

| 认证 ID | 专家 | 能力域 | 状态 | 认证证据 | 审计人 | 有效期 |
|---|---|---|---|---|---|---|
| CERT-AOEM-PT-001 | 庞统 | AOEM_Theory | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-AOEM-PT-002 | 庞统 | AOEM_Runtime | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-AOEM-PT-003 | 庞统 | AOEM_GPU | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-AOEM-PT-004 | 庞统 | AOEM_Privacy | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-MATH-HT-001 | 华佗 | 代数结构 | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-MATH-HT-002 | 华佗 | 代数语义 | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-LANG-ZZ-001 | 庄周 | 语言设计 | UNCERTIFIED | 待填写 | 赵云 | 待填写 |
| CERT-LANG-ZZ-002 | 庄周 | 编译原理 | UNCERTIFIED | 待填写 | 赵云 | 待填写 |

## 5. 审计规则

1. 认证状态不是 `CERTIFIED` 时，专家不得接对应领域生产任务。
2. 认证过期必须重新训练。
3. 认证暂停时，所有相关任务必须进入复审。
4. 认证证据不足时，赵云必须 FAIL。
