# OpenAI Provider Adapter

OpenAI is a model provider target for future Runtime execution.

Runtime V2.6 keeps this adapter disabled until credentials, model policy, budget policy, and output audit policy are explicitly configured.

Expected invocation shape:

```python
result = provider.invoke(
    role="agent_id",
    task=task_packet,
    context=runtime_context,
)
```

No API keys are stored in this repository.
