# OMCF Command Center 傻瓜使用手册

打开地址：

```text
http://127.0.0.1:8765
```

这个页面不是普通看板，而是 OMCF 的安全指挥台。

## 先看顶部四个数字

| 英文 | 中文解释 | 怎么看 |
|---|---|---|
| Running Agents | 正在运行的AI角色 | 数字越大，说明当前有更多角色参与过任务 |
| Safe Ready | 已经通过门禁、可进入安全执行的命令 | 可以点“安全执行”的命令数量 |
| Commands / Queue | 命令总数 / 安全队列数量 | 前面是已创建命令，后面是等待Worker处理 |
| Worker Done | Worker已完成任务 | 已完成低风险文档闭环的数量 |

## 左侧菜单怎么用

| 菜单 | 中文意思 | 用途 |
|---|---|---|
| 组织树 | AI公司组织架构 | 看女娲、诸葛亮、墨子、赵云等角色状态 |
| 任务流 | 当前任务列表 | 启动任务，查看任务追踪 |
| 对话轨迹 | Agent协作记录 | 看谁调用了哪个Provider，生成了什么 |
| Human Queue | 人工审批队列 | 批准、拒绝、打回需要人工确认的事项 |
| Metrics | 运行指标 | 看角色调用次数、成功率、审批次数 |
| Provider 链 | 工具/模型调用来源 | 看 Codex、GitHub、GPT、AOEM 等Provider状态 |
| 使用教程 | 页面内教程 | 不懂按钮含义时先看这里 |

## 最常用流程

1. 打开“任务流”。
2. 找到你要做的任务。
3. 点“启动”。
4. 点“查看命令日志”。
5. 看这条命令是否通过 Dry Run。
6. 如果需要 King Xu 批准，就点“King Xu 批准”。
7. 如果需要赵云审计，就点“赵云审计通过”。
8. 如果显示 `READY_FOR_SAFE_EXECUTION`，点“安全执行”。
9. 如果显示 `SAFE_EXECUTION_QUEUED`，低风险文档任务可以点“Worker 执行”。
10. Worker 完成后，输出会进入项目记忆。

## 按钮解释

| 按钮 | 中文意思 | 会发生什么 |
|---|---|---|
| 启动下一任务 | 创建一条新命令 | 只写命令日志，不直接执行生产动作 |
| 启动 | 启动某个任务 | 创建该任务的命令并自动Dry Run |
| Trace | 追踪 | 查看任务全过程日志 |
| 日志 | 角色日志 | 查看某个Agent做过什么 |
| Dry Run | 试跑 | 判断风险，不真正执行 |
| King Xu 批准 | 人工批准 | 记录你允许继续 |
| 赵云审计通过 | 审计通过 | 记录审计官允许继续 |
| 安全执行 | 进入安全执行队列 | 只写入Safe Execution Queue |
| Worker Dry Run | Worker试跑 | 检查Worker能不能处理该命令 |
| Worker 执行 | Worker执行低风险任务 | 只允许文档类低风险任务执行 |
| 拒绝 | 阻断 | 记录拒绝，后续不能继续 |
| 打回 | 退回修改 | 记录需要修改后再来 |

## 状态解释

| 状态 | 中文意思 |
|---|---|
| READY_FOR_SAFE_EXECUTION | 已经通过门禁，可以安全执行 |
| SAFE_EXECUTION_QUEUED | 已进入安全执行队列 |
| WAIT_HUMAN_APPROVAL | 等待King Xu批准 |
| WAIT_AUDIT_PASS | 等待赵云审计 |
| BLOCKED_PRODUCTION_DEFAULT_DENY | 生产任务默认禁止 |
| WORKER_COMPLETED | Worker已完成 |
| WORKER_REJECTED | Worker拒绝处理 |
| PROVIDER_EXECUTED | Provider真实执行成功 |

## Worker 能做什么

Worker Alpha 只允许做三件事：

1. 生成文档。
2. 调用 Codex 生成方案。
3. 写入项目记忆。

输出位置：

```text
MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Safe_Execution_Worker_Alpha/
```

## Worker 不能做什么

Worker Alpha 禁止：

- 改数据库。
- 连银行或支付接口。
- 执行 AOEM 核心能力。
- 部署生产环境。
- 删除文件。
- 修改生产系统。

## 一句话记住

```text
看不懂就先点 Trace，不确定就只点 Dry Run。
```

真正执行前必须看到：

```text
READY_FOR_SAFE_EXECUTION
```

低风险文档任务才可以继续点：

```text
Worker 执行
```
