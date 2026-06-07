# OMCF Alpha Run 001 Manifest

## Basic Information

- Run ID: OMCF-ALPHA-001
- Project: 株洲物业监管平台
- Date: 2026-06-08
- Runtime baseline: OMCF Runtime V2.6 frozen baseline
- Goal: verify the first real provider chains
- Human owner: King Xu

## Provider Chain Targets

| Chain | Target | Result |
|---|---|---|
| 诸葛亮 -> Codex | Generate real project task plan | PROVIDER_EXECUTED |
| 嬴政 -> GPT | Generate PRD through GPT API | BLOCKED_OPENAI_API_KEY_MISSING |
| 赵云 -> GitHub | Inspect real GitHub repository state | PROVIDER_EXECUTED |

## Alpha Boundary

This run does not upgrade Runtime.

This run does not:

1. Add roles.
2. Add protocols.
3. Change database schema.
4. Touch bank, payment, property registration, or fund interfaces.
5. Train AI models.
6. Execute AOEM runtime logic.
7. Deploy to production.

## Evidence Files

| Evidence | Path |
|---|---|
| Provider invocation log | 01_alpha_provider_invocations.jsonl |
| Provider readiness | 02_provider_readiness.md |
| Codex task plan | 03_zhuge_codex_task_plan.md |
| GPT blocked report | 04_yingzheng_gpt_blocked_report.md |
| GitHub audit | 05_zhaoyun_github_audit.md |
| Alpha audit report | 06_alpha_audit_report.md |

## Overall Result

```text
PARTIAL_SUCCESS_BLOCKED_BY_GPT_PROVIDER_CONFIG
```

Codex and GitHub provider chains were executed with real local/GitHub evidence.

GPT provider chain was not executed because no OpenAI-compatible API configuration is present in the environment.
