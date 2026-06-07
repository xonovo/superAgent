# OMCF Production Run 001 Manifest

## Basic Information

- Run ID: OMCF-PRUN-001
- Project: 株洲物业监管平台
- Date: 2026-06-07
- Runtime baseline: OMCF Runtime V2.6 frozen baseline
- Provider: provider.codex.manual
- Provider execution channel: current Codex session
- Provider status: PROVIDER_EXECUTED
- Human owner: King Xu
- Audit role: 赵云 / AUD-001

## Production Run Goal

Complete the first real provider-backed production run for the Zhuzhou Property Supervision Platform.

The run must produce:

1. Project startup record.
2. ZhugeLiang task tree.
3. Mozi architecture tree.
4. YingZheng PRD.
5. LuBan database analysis.
6. XiangYu data quality analysis.
7. ZhaoYun audit report.

## Execution Boundary

This run performs real Codex provider work and writes concrete project artifacts.

This run does not:

1. Write business application code.
2. Change database schemas.
3. Connect to bank, payment, property registration, or fund systems.
4. Train or modify AI models.
5. Execute AOEM core logic.
6. Deploy to production.

## Evidence

| Evidence | Path |
|---|---|
| Runtime freeze | OMCF_Runtime/V2_6_FREEZE.md |
| Provider invocations | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/01_real_provider_invocations.jsonl |
| Task tree | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/02_zhuge_task_tree.md |
| Architecture tree | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/03_mozi_architecture_tree.md |
| PRD | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/04_yingzheng_prd.md |
| Database analysis | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/05_luban_database_analysis.md |
| Data quality analysis | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/06_xiangyu_data_quality_analysis.md |
| Audit report | MCP/17_Memory_Center/Project_Memory/Zhuzhou_Property_Platform/Production_Run_001/07_zhaoyun_audit_report.md |

## Input References

1. MCP/README.md
2. MCP/AGENT_ROLE_MATRIX.md
3. MCP/PROJECT_PACK_TEMPLATE.md
4. MCP/TASK_FLOW.md
5. MCP/01_Product/prd_outline.md
6. MCP/02_Architecture/architecture_principles.md
7. MCP/03_Database/data_domain_map.md
8. MCP/12_Data_Governance/data_governance_plan.md
9. MCP/09_Audit/audit_report_template.md
10. OMCF_Runtime/providers/providers.json
