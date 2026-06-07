# 赵云 -> True GitHub Audit

## Provider

- Provider: provider.github.app
- Secondary evidence: git SSH remote
- Status: PROVIDER_EXECUTED
- Mock: false
- Simulated: false

## Git Remote Evidence

| Check | Result |
|---|---|
| Remote | `git@github.com:xonovo/superAgent.git` |
| Local HEAD before Alpha artifacts | `1cfb31b` |
| Remote `origin/main` before Alpha artifacts | `1cfb31bbc517782274e77699bc102f31e3449f76` |
| Remote HEAD before Alpha artifacts | `1cfb31bbc517782274e77699bc102f31e3449f76` |
| Local tree before Alpha artifacts | clean |

## GitHub App Evidence

| Field | Value |
|---|---|
| Repository | `xonovo/superAgent` |
| Repository ID | `1261859827` |
| Owner | `xonovo` |
| Visibility | `public` |
| Default branch | `main` |
| Archived | `false` |
| Permission admin | `true` |
| Permission maintain | `true` |
| Permission pull | `true` |
| Permission push | `true` |
| Permission triage | `true` |

## Fetched Evidence

The GitHub App successfully fetched:

```text
https://github.com/xonovo/superAgent/blob/main/OMCF_Runtime/V2_6_FREEZE.md
```

Fetched title:

```text
V2_6_FREEZE.md
```

Fetched modified date:

```text
2026-06-07T13:38:12Z
```

## GitHub CLI Boundary

`gh` is installed, but not authenticated.

Result:

```text
gh auth status -> not logged in
```

Therefore:

1. GitHub App metadata inspection is available.
2. Git SSH remote operations are available.
3. GitHub CLI PR/Issue workflows are blocked until `gh auth login` or `GH_TOKEN`.

## Audit Conclusion

GitHub provider chain is real and partially operational:

```text
PROVIDER_EXECUTED_FOR_REPO_METADATA_AND_REMOTE_EVIDENCE
```

PR/Issue audit is not claimed in this run.
