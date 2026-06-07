# Runtime Engine

本目录包含 OMCF Runtime 的执行引擎。

## 命令

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2-5 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py start-project-v2-6 --project-name "株洲物业监管平台" --project-code "demo_property" --project-type "政务 / 物业监管 / 数据平台"
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-tools
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-providers
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-human-queue
```

```powershell
python OMCF_Runtime/runtime/omcf_runtime.py list-metrics
```

## 输出

Runtime V1 会生成：

1. Runtime Context
2. 女娲启动记录
3. 诸葛亮任务树
4. 墨子架构树
5. 嬴政文档树
6. 赵云审计报告

Runtime V2 额外生成：

1. Tool Registry
2. Tool Layer Report
3. Agent Call Packets
4. Tool Invocations JSONL

Runtime V2.5 额外生成：

1. Provider Registry
2. Provider Execution Plan
3. Human Approval Requests
4. Human Approval Report

Runtime V2.6 额外生成：

1. Provider Adapter Results
2. Human Queue Entries
3. Metrics Report
4. Local aggregate metrics
