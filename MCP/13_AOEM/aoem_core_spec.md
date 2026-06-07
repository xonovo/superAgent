# AOEM Core Spec

## 1. 定位

AOEM 是 OMCF 中的内核与执行能力层，负责为 AI Agent、数据蒸馏、代数执行、GPU 调度和隐私计算提供底层能力。

## 2. 能力边界

AOEM-Codex 可以输出：

1. 内核能力说明。
2. 执行链路设计。
3. 插件或扩展机制草案。
4. GPU 调度策略。
5. 隐私计算边界。
6. 性能优化建议。

AOEM-Codex 不得直接决定：

1. 业务流程。
2. 数据结构。
3. 外部接口协议。
4. 生产发布。
5. 未经审计的自动决策。

## 3. 核心执行逻辑要求

任何核心执行逻辑必须说明：

1. 输入对象。
2. 输出对象。
3. 状态变化。
4. 错误路径。
5. 超时和重试策略。
6. 审计日志点。
7. 回滚或降级策略。

## 4. 验证要求

AOEM 任务至少提供一种验证方式：

1. `GPU_dispatch_test`
2. `privacy_boundary_test`
3. `execution_determinism_test`
4. `runtime_regression_test`
5. `performance_baseline_test`

## 5. 审批要求

涉及核心执行逻辑、隐私计算边界、生产 GPU 调度的变更，必须进入 L6 审计，并由 King Xu 人工确认。
