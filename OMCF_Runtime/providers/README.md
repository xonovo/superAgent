# Provider Layer

Provider Layer decouples OMCF agents from the systems that actually execute work.

An OMCF agent is a role definition:

```text
agent profile + knowledge scope + capability gates + output contract
```

A provider is an execution backend:

```text
Codex, GPT, Claude, local LLM, AOEM, or another tool runtime
```

Runtime V2.6 records provider assignments, invocation contracts, and adapter execution results. It does not hardcode model-specific behavior into agent logic.

## Registry

Provider definitions live in:

```text
OMCF_Runtime/providers/providers.json
```

Each provider declares:

1. Provider identity.
2. Execution mode.
3. Whether the adapter is enabled.
4. Whether human approval is required.
5. Supported capabilities.
6. Adapter path.

External adapters can be enabled later without changing the agent registry.
