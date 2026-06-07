# 鲁班七号数据库分析

## Scope

This analysis defines database domains and inventory requirements.

It does not execute DDL, migration, deletion, schema change, or production data access.

Any historical database structure change requires King Xu approval.

## Core Data Domains

| Domain | Key Objects | Notes |
|---|---|---|
| Person | owner, contact person, enterprise representative | Sensitive data; requires privacy classification |
| House | house, room, property right, use purpose | Core supervision object |
| Community | community, building, unit, floor | Must preserve hierarchy |
| Property enterprise | enterprise, service contract, service area | Connects enterprise and community |
| Contract | service contract, owner committee agreement | Needs effective date and audit status |
| Fee | fee item, receivable, payment, arrears | Bank/payment integration protected |
| Public income | income source, allocation, disclosure | Requires traceability |
| Maintenance fund | account, contribution, usage, approval | Protected fund domain |
| Bank flow | transaction, reconciliation, exception | Protected interface domain |
| Property registration | registration record, owner-house relation | External official source |
| Complaint and event | complaint, risk event, handling result | Supports risk supervision |
| Audit log | operation, data change, interface, AI output | Cross-domain requirement |

## Recommended Storage Layers

```text
raw_source_snapshot
  -> staging_import
    -> standard_domain
      -> business_view
        -> report_mart
          -> audit_archive
```

## First Inventory Checklist

1. List all historical databases and schemas.
2. List table names, row counts, primary keys, and update frequency.
3. Identify source systems for house, community, enterprise, owner, fee, bank flow, and registration data.
4. Identify fields with personal information.
5. Identify fields used for financial or fund decisions.
6. Identify current duplicate keys and missing primary keys.
7. Export data dictionary if available.
8. Record current backup, rollback, and retention rules.

## Conceptual Entity Relations

```text
Community
  -> Building
    -> Unit
      -> House
        -> PersonHouseRelation
          -> Person

PropertyEnterprise
  -> ServiceContract
    -> Community

House
  -> FeeLedger
  -> PublicIncomeAllocation
  -> MaintenanceFundRecord
  -> ComplaintEvent
  -> AuditLog
```

## Database Red Lines

1. Do not delete historical databases.
2. Do not overwrite historical systems.
3. Do not run migration scripts before inventory and approval.
4. Do not connect bank or fund systems before audit log and reconciliation rules are defined.
5. Do not use unreviewed production data for AI training.

## Data Dictionary Minimum Fields

Every field must record:

1. Field name.
2. Chinese name.
3. Data type.
4. Required flag.
5. Unique flag.
6. Source system.
7. Business meaning.
8. Security level.
9. AI feature eligibility.
10. Audit requirement.

## Initial Database Risk Assessment

| Risk | Level | Impact | Required Action |
|---|---|---|---|
| No confirmed historical schema inventory | High | Blocks real database design | Collect schema inventory |
| House unique identifier may be inconsistent | High | Causes duplicates and wrong relation mapping | Define canonical house key |
| Person-house relation may be incomplete | High | Affects supervision and ownership analysis | Profile missing owner/related person fields |
| Bank and fee ledgers may not reconcile | High | Fund supervision risk | Define reconciliation rules before integration |
| Sensitive fields may lack classification | High | Privacy and compliance risk | Classify and mask before broader use |
