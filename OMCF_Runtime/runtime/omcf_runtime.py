from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "OMCF_Runtime"
MCP_ROOT = REPO_ROOT / "MCP"


REQUIRED_AGENTS = [
    "nuwa.yaml",
    "zhuge_liang.yaml",
    "mozi.yaml",
    "yingzheng.yaml",
    "zhaoyun.yaml",
]

REQUIRED_MCP_FILES = [
    "README.md",
    "PROJECT_PACK_TEMPLATE.md",
    "TASK_CARD_TEMPLATE.md",
    "TASK_FLOW.md",
    "AUDIT_GATE_RULES.md",
    "20_Expert_Training/capability_matrix.md",
    "20_Expert_Training/knowledge_certification.md",
    "16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md",
    "17_Memory_Center/decision_registry.md",
]


@dataclass
class AgentSpec:
    id: str
    name: str
    nickname: str
    role: str
    responsibility: str
    capabilities: list[str]
    knowledge: list[str]
    outputs: list[str]


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value:
                data[key] = value
            else:
                data[key] = []
            continue
    return data


def load_agents() -> dict[str, AgentSpec]:
    agents_dir = RUNTIME_ROOT / "agents"
    agents: dict[str, AgentSpec] = {}
    for filename in REQUIRED_AGENTS:
        path = agents_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing agent spec: {path}")
        raw = parse_simple_yaml(path)
        agent = AgentSpec(
            id=str(raw.get("id", "")),
            name=str(raw.get("name", "")),
            nickname=str(raw.get("nickname", "")),
            role=str(raw.get("role", "")),
            responsibility=str(raw.get("responsibility", "")),
            capabilities=list(raw.get("capabilities", [])),
            knowledge=list(raw.get("knowledge", [])),
            outputs=list(raw.get("outputs", [])),
        )
        agents[agent.id] = agent
    return agents


def check_required_files() -> list[str]:
    missing: list[str] = []
    for rel in REQUIRED_MCP_FILES:
        if not (MCP_ROOT / rel).exists():
            missing.append(f"MCP/{rel}")
    return missing


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_runtime_context(project_name: str, project_code: str, project_type: str, agents: dict[str, AgentSpec]) -> dict[str, Any]:
    return {
        "runtime": "OMCF_Runtime_V1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project": {
            "name": project_name,
            "code": project_code,
            "type": project_type,
            "phase": "Phase-1 文档建设",
        },
        "chain": [
            "CAIO-001",
            "PM-001",
            "ARC-001",
            "DOC-001",
            "AUD-001",
        ],
        "agents": {
            agent_id: {
                "name": agent.name,
                "nickname": agent.nickname,
                "role": agent.role,
                "capabilities": agent.capabilities,
            }
            for agent_id, agent in agents.items()
        },
        "gates": {
            "capability_matrix": "MCP/20_Expert_Training/capability_matrix.md",
            "knowledge_certification": "MCP/20_Expert_Training/knowledge_certification.md",
            "aoem_constitution": "MCP/16_Knowledge_Base/AOEM/AOEM_CONSTITUTION.md",
            "decision_registry": "MCP/17_Memory_Center/decision_registry.md",
        },
    }


def render_nuwa(project_name: str, project_code: str, project_type: str, agent: AgentSpec) -> str:
    return f"""
# 01 女娲启动记录

- Agent：{agent.nickname} / {agent.id}
- 项目名称：{project_name}
- 项目代号：{project_code}
- 项目类型：{project_type}
- 当前阶段：Phase-1 文档建设

## 启动判断

1. OMCF 制度层已存在。
2. Runtime V1 进入项目启动链路。
3. 本次运行不写业务代码。
4. 项目记忆不预设槽位，仅在正式项目启动时按需创建。
5. 任务分配必须检查 Capability Matrix 和 Knowledge Certification。

## 调度链路

```text
女娲 -> 诸葛亮 -> 墨子 -> 嬴政 -> 赵云
```
"""


def render_task_tree(project_name: str, project_code: str, agent: AgentSpec) -> str:
    return f"""
# 02 诸葛亮任务树

- Agent：{agent.nickname} / {agent.id}
- 项目：{project_name}

## Phase-1 任务树

| 任务编号 | 任务名称 | 责任角色 | 输出物 | 状态 |
|---|---|---|---|---|
| {project_code.upper()}-TASK-001 | 项目资料包确认 | 诸葛亮 | Project Pack Review | READY |
| {project_code.upper()}-TASK-002 | 知识库检索 | 伏羲 | Knowledge Gap Report | READY |
| {project_code.upper()}-TASK-003 | 项目记忆检索 | 仓颉 | Memory Retrieval Report | READY |
| {project_code.upper()}-TASK-004 | 能力矩阵检查 | 诸葛亮 / 赵云 | Capability Gate Report | READY |
| {project_code.upper()}-TASK-005 | 架构树生成 | 墨子 | Architecture Tree | READY |
| {project_code.upper()}-TASK-006 | 文档树生成 | 嬴政 | Document Tree | READY |
| {project_code.upper()}-TASK-007 | 启动审计 | 赵云 | Audit Report | READY |

## 分配原则

1. 不按昵称直接派活，先查能力矩阵。
2. 未认证知识域不得承接生产任务。
3. AOEM 任务必须遵守 AOEM Constitution。
4. 审计失败必须进入 Failure Log。
"""


def render_architecture_tree(project_name: str, project_type: str, agent: AgentSpec) -> str:
    return f"""
# 03 墨子架构树

- Agent：{agent.nickname} / {agent.id}
- 项目：{project_name}
- 项目类型：{project_type}

## 架构树 V1

```text
Project
├── Product Boundary
├── Architecture Boundary
├── Data Boundary
├── API Boundary
├── UI Boundary
├── AI Boundary
├── Server Boundary
├── Audit Boundary
└── Deployment Boundary
```

## 能力门禁

| 门禁 | 状态 | 说明 |
|---|---|---|
| Capability Matrix | REQUIRED | 分配任务前必须检查 |
| Knowledge Certification | REQUIRED | 未认证不得承接生产任务 |
| AOEM Constitution | CONDITIONAL | 涉及 AOEM 时必须检查 |
| Decision Registry | REQUIRED | 重大选择和拒绝方案必须登记 |

## 架构结论

当前仅生成项目启动架构树，不进入业务模块实现。
"""


def render_document_tree(project_name: str, agent: AgentSpec) -> str:
    return f"""
# 04 嬴政文档树

- Agent：{agent.nickname} / {agent.id}
- 项目：{project_name}

## 文档树 V1

```text
Project Documents
├── 00_Project_Charter
├── 01_Product
├── 02_Architecture
├── 03_Database
├── 04_API
├── 05_UI
├── 06_AI
├── 07_Server
├── 08_Test
├── 09_Audit
└── 10_Deployment
```

## Runtime 产物

1. Runtime Context
2. Project Bootstrap
3. Task Tree
4. Architecture Tree
5. Document Tree
6. Audit Report
"""


def render_audit_report(project_name: str, missing_files: list[str], agent: AgentSpec) -> str:
    status = "PASS" if not missing_files else "FAIL"
    missing_text = "\n".join(f"- {item}" for item in missing_files) if missing_files else "- 无"
    return f"""
# 05 赵云启动审计报告

- Agent：{agent.nickname} / {agent.id}
- 项目：{project_name}
- 审计结论：{status}

## 审计范围

1. Agent Registry 完整性。
2. MCP 关键制度文件存在性。
3. Capability Matrix 引用。
4. Knowledge Certification 引用。
5. AOEM Constitution 引用。
6. Decision Registry 引用。

## 缺失文件

{missing_text}

## 审计意见

{"启动链路可进入下一步任务规划。" if status == "PASS" else "存在关键文件缺失，不得进入下一步。"}
"""


def start_project(project_name: str, project_code: str, project_type: str, output_dir: str | None) -> Path:
    agents = load_agents()
    missing_files = check_required_files()
    run_id = f"{project_code}_{timestamp()}"
    out_dir = Path(output_dir) if output_dir else RUNTIME_ROOT / "tasks" / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    context = build_runtime_context(project_name, project_code, project_type, agents)
    context["run_id"] = run_id
    context["status"] = "AUDIT_PASS" if not missing_files else "AUDIT_FAIL"

    write_json(out_dir / "00_runtime_context.json", context)
    write_text(out_dir / "01_nuwa_project_bootstrap.md", render_nuwa(project_name, project_code, project_type, agents["CAIO-001"]))
    write_text(out_dir / "02_zhuge_task_tree.md", render_task_tree(project_name, project_code, agents["PM-001"]))
    write_text(out_dir / "03_mozi_architecture_tree.md", render_architecture_tree(project_name, project_type, agents["ARC-001"]))
    write_text(out_dir / "04_yingzheng_document_tree.md", render_document_tree(project_name, agents["DOC-001"]))
    write_text(out_dir / "05_zhaoyun_audit_report.md", render_audit_report(project_name, missing_files, agents["AUD-001"]))

    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="OMCF Runtime V1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start-project", help="Start a project bootstrap chain")
    start.add_argument("--project-name", required=True)
    start.add_argument("--project-code", required=True)
    start.add_argument("--project-type", required=True)
    start.add_argument("--output-dir", default=None)

    args = parser.parse_args()

    if args.command == "start-project":
        out_dir = start_project(args.project_name, args.project_code, args.project_type, args.output_dir)
        print(f"OMCF Runtime V1 completed: {out_dir}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
