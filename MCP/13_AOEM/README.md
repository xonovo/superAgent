# 13_AOEM

本目录归属 AOEM-Codex（庞统 / AOEM-001），用于沉淀 AOEM 内核、GPU 调度、隐私计算、代数执行和执行优化相关规范。

## 职责范围

1. AOEM 内核能力边界。
2. 执行引擎、运行时和扩展能力设计。
3. GPU 调度、资源隔离、任务优先级和降级策略。
4. 隐私计算、数据最小化和敏感数据边界。
5. 代数执行与 AI 推理链路的性能优化。

## 核心文档

| 文档 | 说明 |
|---|---|
| `aoem_core_spec.md` | AOEM 内核能力与边界规范 |
| `gpu_dispatch_policy.md` | GPU 调度策略 |
| `privacy_compute_policy.md` | 隐私计算策略 |
| `execution_optimization.md` | 执行优化规范 |
| `aoem_task_template.md` | AOEM 专项任务模板 |

## 审计要求

1. AOEM 核心执行逻辑必须由赵云审计。
2. GPU 调度和部署相关事项必须由张飞技术复核。
3. 架构边界变化必须由墨子审批。
4. 涉及生产、隐私计算或不可逆执行路径时必须由 King Xu 人工确认。
