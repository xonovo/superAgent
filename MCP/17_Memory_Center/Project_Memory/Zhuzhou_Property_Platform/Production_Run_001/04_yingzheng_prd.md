# 嬴政 PRD V0.1

## Product Positioning

株洲物业监管平台 is a supervision and data governance platform for housing authorities and related units to manage property enterprises, communities, houses, fees, public income, maintenance funds, risk events, and data quality.

This PRD is V0.1. It is based on existing OMCF knowledge documents and must be refined after King Xu provides the full Project Pack.

## Target Users

| User | Goal |
|---|---|
| Housing authority supervisor | View supervision dashboard, risk alerts, enterprise compliance, fund status |
| Business department operator | Manage house, community, enterprise, event, and supervision records |
| Data governance operator | Profile data, identify duplicates, track quality issues, prepare correction lists |
| Audit officer | Review operation logs, data changes, interface logs, AI outputs, release evidence |
| Property enterprise user | Submit or verify assigned enterprise/community data after permission approval |
| Leadership viewer | Review macro indicators, risk trend, rectification progress, and supervision reports |

## Product Modules

1. Supervision dashboard.
2. House data management.
3. Community and building management.
4. Property enterprise management.
5. Owner and person-house relationship management.
6. Fee and fund supervision.
7. Public income supervision.
8. Maintenance fund supervision.
9. Complaint, event, and risk management.
10. External interface management.
11. Audit log center.
12. AI advisory and data profiling center.

## MVP Scope

| Module | MVP Scope |
|---|---|
| Supervision dashboard | Core indicators, data quality overview, risk summary, pending review count |
| House data | House list, hierarchy, source system, quality status, audit trail |
| Community data | Community, building, unit, property service coverage |
| Enterprise data | Enterprise profile, service contract, supervision status |
| Data governance | Field mapping, duplicate detection, missing value report, anomaly list |
| Audit | Operation log, data change log, AI output log, provider execution log |

## Out of Scope for V0.1

1. Production database migration.
2. Bank or payment integration.
3. Automatic fund decision.
4. AI model training.
5. AOEM execution.
6. Production deployment.

## Key Workflows

### Data Intake Workflow

```text
Source material
  -> Staging import
    -> Field mapping
      -> Quality profiling
        -> Issue list
          -> Manual review
            -> Standardized domain data
              -> Audit record
```

### Supervision Workflow

```text
Data update
  -> Rule check
    -> Risk signal
      -> Supervisor review
        -> Rectification task
          -> Evidence upload
            -> Audit close
```

### AI Advisory Workflow

```text
Business question
  -> Knowledge retrieval
    -> AI advisory output
      -> Human review
        -> Business decision
          -> Audit log
```

## Acceptance Criteria for Phase-1

1. Project scope and protected scopes are documented.
2. Logical architecture and module boundaries are documented.
3. Database domain map and quality checks are documented.
4. PRD V0.1 covers user roles, modules, workflows, and exclusions.
5. No protected action is executed without King Xu approval.
6. ZhaoYun audit report is completed.

## Open Questions

1. Which historical systems currently hold house and property enterprise data?
2. Is the 660k house dataset already exported, or still inside existing systems?
3. Which bank, payment, property registration, and fund systems must integrate?
4. What are the official reporting indicators required by housing authorities?
5. Which departments can approve corrections to house-owner relationships?
6. Which data fields are sensitive and require masking or tiered access?
