# OMC-OS Product Blueprint

## Naming

```text
OMCF = OneMan AI Company Framework
OMC-OS = OneMan AI Company Operating System
```

OMCF is the framework name. It defines the AI company organization, roles,
rules, memory, knowledge, audit, and execution boundaries.

OMC-OS is the product direction. It turns OMCF into an AI Agent project
operating system.

## Product Positioning

OMC-OS is not a code IDE. It is an AI Agent project operating system.

Its job is to let one human decision maker manage many AI Agents across many
projects through:

1. Project creation.
2. Project material import.
3. Agent Pool binding.
4. Task dispatch.
5. Human approval.
6. Audit gates.
7. Safe execution.
8. Project memory writeback.

## Layer Model

```text
OMC-OS
|-- Company Layer
|   |-- Agent Pool
|   |-- Capability Matrix
|   |-- Knowledge Base
|   `-- Global Memory
|
|-- Workspace Layer
|   `-- Multi-project management
|
|-- Project Layer
|   |-- Project Pack
|   |-- Project Memory
|   |-- Project Tasks
|   |-- Project Outputs
|   `-- Project Audit
|
|-- Runtime Layer
|   |-- Task Engine
|   |-- Provider Router
|   |-- Human Queue
|   `-- Safe Execution Worker
|
`-- Dashboard Layer
    |-- Command Center
    |-- Agent Timeline
    |-- Task Trace
    `-- Metrics
```

## Workspace

A workspace is the top-level working area, similar to a VS Code workspace.

Example:

```text
Workspace:
KingXu_AI_Company
```

The workspace can contain multiple projects, but projects must not be created as
empty pre-filled slots.

Correct:

```text
User clicks New Project
  -> Project directory is created
  -> Project Pack is initialized
  -> Project Memory starts empty
```

Incorrect:

```text
Pre-create NOVOVM, Wallet, Official_Website, AOEM, or other empty project slots.
```

Reason:

```text
Empty project slots pollute memory and create zombie projects.
```

## Project

Each project should be isolated.

Future project structure:

```text
projects/
`-- <Project_Code>/
    |-- project_pack/
    |-- memory/
    |-- tasks/
    |-- outputs/
    |-- audit/
    `-- providers/
```

Current repository compatibility:

```text
MCP/17_Memory_Center/Project_Memory/<Project_Code>/
```

The current Zhuzhou Property Platform project is the first real project memory.
It is not a reusable empty template.

## Agent Pool

Agents are company-level shared resources.

Examples:

```text
女娲
诸葛亮
墨子
鲁班七号
赵云
庞统
华佗
庄周
```

Agents do not belong to one project. They are bound to a project context at
runtime.

## Project Binding

The same Agent becomes project-specific after binding to a project pack.

Example:

```text
诸葛亮 + 株洲物业项目资料 = 株洲项目经理
诸葛亮 + NOVOVM项目资料 = NOVOVM项目经理
```

The role is shared. The memory and context are project-specific.

## Command Center

The Command Center should eventually support:

1. New Project.
2. Open Project.
3. Close Project.
4. Import Materials.
5. Start Agent.
6. View Tasks.
7. Approve Tasks.
8. View Audit Reports.
9. View Execution Logs.
10. View Provider Calls.

Current Dashboard Alpha already supports:

1. Agent status.
2. Task flow.
3. Human Queue.
4. Metrics.
5. Provider chain.
6. Command Center.
7. Safe Execution Gates.
8. Safe Execution Worker Alpha.

## Reuse Workflow

The final workflow should be:

```text
New Project
  -> Import Project Materials
  -> Bind Agent Pool
  -> Start Project
  -> OMC-OS dispatches Agents
  -> King Xu approves critical gates
  -> Zhao Yun audits results
  -> Worker writes safe outputs to Project Memory
```

This is the core reuse value.

You do not rebuild the AI team for every project.

You create a new project context and reuse the same AI company.
