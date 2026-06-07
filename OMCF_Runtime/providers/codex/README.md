# Codex Provider Adapter

Codex is the default manual handoff provider for Runtime V2.6.

This adapter is intentionally explicit:

1. Runtime creates a provider invocation.
2. Runtime records the agent packet, provider route, and output contract.
3. Codex or the current operator can execute the task using the generated packet.
4. The result must return to the audit chain before downstream execution.

The adapter does not bind any OMCF agent to Codex permanently. Agents remain profiles; Codex is only one provider implementation.
