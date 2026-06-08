# OMC-OS Workbench 傻瓜使用手册

## OMCF 是什么

```text
OMCF = OneMan AI Company Framework
一人AI公司框架
```

它的意思是：

```text
一个人作为最终决策者
通过一套 AI 组织、任务、审计、记忆、知识和执行系统
管理多个 AI Agent 完成项目
```

现在它已经不只是 Framework，更接近：

```text
OMC-OS = OneMan AI Company Operating System
一人AI公司操作系统
```

你可以这样理解：

```text
OMCF 是制度和框架
OMCF Runtime 是运行时
OMC-OS Workbench 是用户界面
OMC-OS 是最终产品形态
```

打开地址：

```text
http://127.0.0.1:8765
```

这个页面不是普通看板，而是 OMCF 的安全指挥台。

## 最终它会像什么

它应该像一个 AI Agent 项目操作系统，而不是普通代码 IDE。

最终使用方式是：

```text
新建项目
→ 导入项目资料
→ 绑定 Agent Pool
→ 启动项目
→ OMCF 调度 Agent 干活
→ King Xu 审批关键节点
→ 赵云审计
→ Worker 写入项目记忆
```

注意：系统不会提前创建 NOVOVM、Wallet、Official_Website 这些空项目槽位。

必须是你点击“新建项目”之后，才创建对应项目目录，避免知识污染。

## 三个核心概念

| 概念 | 中文解释 | 你怎么理解 |
|---|---|---|
| Workspace | 工作区 | 类似 VS Code 工作区，管理多个项目 |
| Project | 项目 | 每个项目有独立资料、任务、记忆、输出、审计 |
| Agent Pool | 智能体池 | 女娲、诸葛亮、墨子、赵云等公司级共享AI角色 |

同一个 Agent 可以服务不同项目：

```text
诸葛亮 + 株洲物业项目资料 = 株洲项目经理
诸葛亮 + NOVOVM项目资料 = NOVOVM项目经理
```

角色共享，项目记忆隔离。

## 现在网页上新增了什么

这次不是只写文档，控制台已经升级为 OMC-OS Workbench Alpha，也就是 AI Agent IDE 的第一版外壳。

新增入口：

| 页面 | 中文解释 | 现在能做什么 |
|---|---|---|
| 工作台 | Workspace 首页 | 看工作区、真实项目、Agent Pool、项目绑定 |
| 项目 | Projects | 看已经存在的项目记忆目录和新项目申请记录 |
| Agent Pool | 智能体池 | 看公司级共享 AI 角色 |
| 项目绑定 | Binding | 看每个 Agent 当前绑定到哪个项目上下文 |

## IDE 四个区域怎么看

| 区域 | 中文解释 | 用途 |
|---|---|---|
| Workspace Tree | 工作区树 | 像 VS Code 左侧目录，只显示真实项目 |
| Project Explorer | 项目资源管理器 | 看 Project Pack、Memory、Tasks、Outputs、Audit |
| Agent Console | 智能体控制台 | 看 Agent 状态和最近协作轨迹 |
| Execution Terminal | 执行终端 | 看 Provider Calls、Audit Logs、Worker Logs、Codex Output |

### 新建项目怎么用

在“工作台”左侧填写：

```text
项目名称
项目代号
```

然后点击：

```text
记录新项目申请
```

注意：

```text
这一步只写 Alpha 申请日志
不会创建项目目录
不会创建空项目槽位
```

真正创建项目目录需要以后单独做：

```text
King Xu 批准
→ 赵云审计
→ Runtime 创建 Project Pack
```

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
