# 墨子架构树

## Project

- Project: 株洲物业监管平台
- Run ID: OMCF-PRUN-001
- Provider: provider.codex.manual
- Provider status: PROVIDER_EXECUTED
- Architecture status: Phase-1 logical architecture only

## Architecture Principle

The platform must separate:

1. Supervision business.
2. Data governance.
3. Fund and external interface integration.
4. AI advisory services.
5. Audit and traceability.

AI outputs must not directly control administrative or fund decisions.

## Logical Architecture

```text
Users
  -> Web/Admin UI
    -> Application Service Layer
      -> Domain Service Layer
        -> Data Access Layer
          -> Core Database
          -> Staging Database
          -> External Systems

AI Service Layer
  -> Knowledge retrieval
  -> Data profiling support
  -> Risk advisory
  -> Human review
  -> Audit log

Audit Layer
  -> Operation logs
  -> Data change logs
  -> Interface logs
  -> AI output logs
  -> Release logs
```

## Domain Boundaries

| Boundary | Scope | Primary Owner |
|---|---|---|
| Organization and permission | Departments, roles, user access, approval authority | 司马懿 |
| Property base data | House, building, unit, community, property relation | 鲁班七号 |
| Property enterprise supervision | Enterprise profile, contracts, service coverage, compliance state | 司马懿 |
| Owner and person profile | Owner, contact, person-house relation, privacy level | 项羽 / 鲁班七号 |
| Fees and funds | Charging ledger, public income, maintenance fund, bank reconciliation | 刘备 / 鲁班七号 |
| Complaints and events | Complaints, disputes, risk events, handling lifecycle | 司马懿 |
| External integration | Bank, payment, property registration, existing government platforms | 刘备 |
| Data governance | Cleansing, deduplication, quality scoring, lineage | 项羽 |
| AI advisory | Risk advisory, feature catalog, RAG, explanation | 王昭君 |
| Audit | Logs, evidence, release gates, AI output audit | 赵云 |

## Recommended Data Flow

```text
Historical systems / external sources
  -> Staging import
    -> Field mapping
      -> Quality profiling
        -> Manual review for sensitive errors
          -> Standardized domain data
            -> Business service
              -> Audit and reporting
```

## Integration Boundaries

1. Property registration data must be imported through a staged and auditable interface.
2. Bank, payment, and fund interfaces must not be connected before signature, reconciliation, exception handling, and audit rules are approved.
3. Historical system replacement is not allowed in Phase-1.
4. Existing databases must be read-only during inventory unless King Xu approves otherwise.
5. Production deployment is out of scope for Production Run 001.

## Technology Direction

| Area | Direction | Reason |
|---|---|---|
| Backend | Modular service architecture | Clear boundaries before microservice split |
| Database | Staging + standardized domain model + audit log | Supports migration safety and traceability |
| Frontend | Admin-first supervision console | Government and operational users need dense workflows |
| AI | Advisory service, not autonomous decision maker | Keeps administrative and fund decisions auditable |
| Runtime | OMCF Runtime V2.6 frozen baseline | Avoid endless control-plane iteration |

## Architecture Decision Candidates

| ADR | Decision | Status |
|---|---|---|
| ADR-ZZW-001 | Use staged import before touching historical data | Proposed |
| ADR-ZZW-002 | Keep AI advisory outputs separate from business decisions | Proposed |
| ADR-ZZW-003 | Treat bank/payment/fund integration as protected scope | Proposed |
| ADR-ZZW-004 | Keep Runtime V2.6 frozen during first production execution | Accepted for this run |
