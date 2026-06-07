# Project Pack V1 Intake Checklist

## Required Materials

- Existing system descriptions, names, screenshots, and ownership.
- Existing database inventory or screenshots: names, table counts, source ownership.
- Status of the 660k house dataset: exported file or still inside historical systems.
- Department list, user roles, approval responsibilities, and permission tiers.
- External system list: bank, payment, property registration, maintenance fund, government platforms.
- Data sensitivity policy, masking rules, and sample export permission.
- Deployment environment constraints.
- Official supervision/reporting indicators and required business workflows.

## Protected Scopes

- No production database migration, DDL, schema change, or data cleaning without explicit approval.
- No bank, payment, fund, or property-registration integration without approval.
- No sensitive data export unless policy and masking requirements are confirmed.
- No automatic fund decisioning.
- No AI output treated as decision authority.
- No AOEM execution.
- No production deployment in this intake phase.

## First Interview Questions

1. Which historical systems currently hold house, community, enterprise, fee, and fund data?
2. Who owns each source system and who can approve data export?
3. Is the 660k house dataset already exported? If yes, in what format?
4. Which departments need daily access, audit access, or leadership-only views?
5. Which fields are sensitive and require masking or tiered permission?
6. Which external interfaces are mandatory for V1.0, and which can wait?
7. What are the official reporting indicators required by the housing authority?
8. Who approves corrections to house-owner or enterprise-service relationships?

## Acceptance Criteria

- Project Pack V1 contains enough source material to replace PRD V0.1 assumptions.
- Scope, protected scopes, user roles, modules, workflows, and exclusions are documented.
- Historical system and database inventories are described from provided materials.
- External interface boundaries and approval gates are listed.
- Data sample policy is confirmed before any sample-based analysis.
- PRD V1.0 and architecture ADR work remain blocked until Project Pack V1 is complete.