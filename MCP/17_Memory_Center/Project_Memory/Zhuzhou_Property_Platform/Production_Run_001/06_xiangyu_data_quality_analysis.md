# 项羽数据质量分析

## Scope

This analysis defines the first data quality framework for the Zhuzhou Property Supervision Platform.

It does not clean production data, train models, or modify source databases.

## Governance Target

The existing governance plan identifies the first governance object as a large house dataset and then extends to people, houses, buildings, communities, property enterprises, fees, bank flows, property registration, and maintenance funds.

## Quality Dimensions

| Dimension | Meaning | Example Check |
|---|---|---|
| Completeness | Required fields are present | House code, community, building, unit, room number |
| Uniqueness | Duplicate records can be identified | Same house appears multiple times |
| Consistency | Data matches across systems | Registration owner matches platform relation |
| Accuracy | Values are reasonable | Area, usage, address, enterprise status |
| Timeliness | Data update time is traceable | Recent fee ledger and enterprise contract status |
| Traceability | Source and transformation are known | Source system and import batch |
| Security level | Sensitive fields are classified | ID number, phone, bank account |
| AI usability | Data can be used safely for features | Feature field has source, quality, and masking status |

## First Batch Quality Checks

| Check ID | Check | Severity |
|---|---|---|
| DQ-001 | House unique identifier exists | High |
| DQ-002 | Community-building-unit-house hierarchy is complete | High |
| DQ-003 | Building area and internal area are non-negative and reasonable | Medium |
| DQ-004 | House purpose field is standardized | Medium |
| DQ-005 | Owner or related person is missing | High |
| DQ-006 | Same house appears more than once | High |
| DQ-007 | Same person linked to multiple houses with unclear relation | Medium |
| DQ-008 | Property registration data differs from platform house data | High |
| DQ-009 | Bank payment data differs from fee ledger | High |
| DQ-010 | Sensitive fields are not classified or masked | High |
| DQ-011 | AI candidate feature lacks source or audit trail | High |

## Quality Workflow

```text
Source data registration
  -> Field mapping
    -> Rule-based profiling
      -> Duplicate and anomaly detection
        -> Quality score
          -> Manual review list
            -> Approved correction plan
              -> Audited correction execution
```

## Suggested Quality Score

| Score Area | Weight |
|---|---|
| Completeness | 20 |
| Uniqueness | 20 |
| Cross-system consistency | 20 |
| Sensitive data classification | 15 |
| Traceability | 15 |
| AI usability | 10 |

## Data Quality Outputs

1. Source dataset inventory.
2. Field mapping table.
3. Required field missing report.
4. Duplicate house report.
5. Person-house relation anomaly report.
6. Registration consistency report.
7. Fee-bank reconciliation exception report.
8. Sensitive field classification report.
9. AI feature eligibility report.

## Human Approval Gates

| Scope | Approval Required |
|---|---|
| Database structure change | Yes |
| Data correction written back to historical system | Yes |
| Bank or fund reconciliation rule affecting business result | Yes |
| AI training data preparation | Yes |
| Sensitive data masking policy change | Yes |

## Open Data Questions

1. What is the canonical house identifier in existing systems?
2. Which system is authoritative for property registration?
3. Which system is authoritative for fee ledger and payment status?
4. Are owner identity fields complete and legally usable?
5. Are public income and maintenance fund records in the same ledger or separate systems?
6. Which fields can be used for AI advisory features after masking?
