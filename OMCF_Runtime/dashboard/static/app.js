const state = {
  snapshot: null,
  activeView: "workbench",
  lastSignature: "",
};

const statusClass = (value, prefix = "status") =>
  `${prefix}-${String(value || "idle").toLowerCase().replaceAll(" ", "_")}`;

const byId = (id) => document.getElementById(id);

const STATUS_ZH = {
  running: "运行中",
  waiting: "等待中",
  audit: "审计中",
  human: "等待人工审批",
  idle: "空闲",
  complete: "已完成",
  blocked: "已阻断",
  queued: "已入队",
  ready: "可安全执行",
  gated: "等待门禁",
  PROVIDER_EXECUTED: "Provider已执行",
  PROVIDER_FAILED: "Provider失败",
  READY_FOR_SAFE_EXECUTION: "可安全执行",
  SAFE_EXECUTION_QUEUED: "已进入安全队列",
  WAIT_HUMAN_APPROVAL: "等待King Xu批准",
  WAIT_AUDIT_PASS: "等待赵云审计",
  WAIT_GATE: "等待门禁",
  BLOCKED_PRODUCTION_DEFAULT_DENY: "生产默认禁止",
  REJECTED: "已拒绝",
  WORKER_COMPLETED: "Worker已完成",
  WORKER_FAILED: "Worker失败",
  WORKER_REJECTED: "Worker已拒绝",
  WORKER_DRY_RUN_PASS: "Worker试跑通过",
  adapter_required: "需要适配器",
  deprecated_alias: "兼容旧名称",
};

const TERM_ZH = {
  "Running Agents": "正在工作的AI角色",
  "Safe Ready": "可进入安全执行的命令",
  "Commands / Queue": "命令总数 / 安全队列",
  "Worker Done": "Worker已完成任务",
  Runs: "运行批次",
  Invocations: "调用次数",
  "Provider Executed": "Provider执行次数",
  "Approval Requests": "审批请求数",
  "Provider success": "Provider成功率",
  Target: "对象",
  Role: "角色",
  Task: "任务",
  Assignee: "负责人",
  Artifact: "产物",
  Command: "命令",
  risk: "风险",
  document: "文档任务",
  code: "代码任务",
  restricted: "受限高风险任务",
  production: "生产任务",
  low: "低风险",
  medium: "中风险",
  high: "高风险",
  critical: "极高风险",
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function agentName(agentId) {
  const agent = state.snapshot?.agents?.find((item) => item.id === agentId);
  return agent ? agent.nickname : agentId;
}

function zhStatus(value) {
  return STATUS_ZH[value] || STATUS_ZH[String(value || "").toLowerCase()] || "";
}

function term(en, zh) {
  return `<span class="term">${escapeHtml(en)}<small>${escapeHtml(zh || TERM_ZH[en] || "")}</small></span>`;
}

function statusPill(value, cssPrefix = "status") {
  return `<span class="${cssPrefix === "status" ? "status-pill" : `${cssPrefix}-status`} ${statusClass(value, cssPrefix)}">${escapeHtml(value)}${zhStatus(value) ? `<small>${escapeHtml(zhStatus(value))}</small>` : ""}</span>`;
}

function renderSummary(snapshot) {
  const running = snapshot.agents.filter((agent) => agent.status === "running").length;
  const queue = snapshot.human_queue.filter((item) => item.queue_status === "pending").length;
  const commands = snapshot.commands?.length || 0;
  const safeReady = snapshot.safe_execution_summary?.ready || 0;
  const safeQueued = snapshot.safe_execution_summary?.queued || 0;
  const workerDone = snapshot.worker_summary?.completed || 0;
  byId("summary-grid").innerHTML = `
    <div class="summary-item">${term("Running Agents")}<strong>${running}</strong></div>
    <div class="summary-item">${term("Safe Ready")}<strong>${safeReady}</strong></div>
    <div class="summary-item">${term("Commands / Queue")}<strong>${commands}/${safeQueued}</strong></div>
    <div class="summary-item">${term("Worker Done")}<strong>${workerDone}</strong></div>
  `;
}

function renderWorkspace(snapshot) {
  const workspace = snapshot.workspace || {};
  const projects = snapshot.projects || [];
  const agents = snapshot.agents || [];
  const bindings = snapshot.agent_bindings || [];
  const activeProject = projects.find((project) => project.code === workspace.active_project_code) || projects[0];
  byId("workspace-tree").innerHTML = renderWorkspaceTree(workspace, projects, agents);
  byId("project-explorer").innerHTML = renderProjectExplorer(snapshot.project_explorer || []);
  byId("agent-console").innerHTML = renderAgentConsole(agents, bindings, snapshot.timeline || []);
  byId("execution-terminal").innerHTML = renderExecutionTerminal(snapshot.execution_terminal || {});
  if (activeProject) {
    byId("project-title").textContent = activeProject.name;
  }
}

function renderWorkspaceTree(workspace, projects, agents) {
  const projectRows = projects
    .map(
      (project) => `
        <button class="tree-node open-project-row" data-project-code="${escapeHtml(project.code)}">
          <span>${project.status === "active" ? "●" : "○"} ${escapeHtml(project.name)}</span>
          <small>${escapeHtml(project.code)}</small>
        </button>
      `,
    )
    .join("");
  return `
    <article class="workspace-card">
      <strong>${escapeHtml(workspace.name || "KingXu_AI_Company")}</strong>
      <div class="workspace-meta">
        <span>${escapeHtml(workspace.product || "OMC-OS Workbench Alpha")}</span>
        <span>真实项目: ${projects.length}</span>
        <span>Agent: ${agents.length}</span>
      </div>
      <div class="workspace-tree">
        <span>workspace/</span>
        <span>|-- projects/</span>
        ${projectRows || `<span>|   \`-- 暂无真实项目</span>`}
        <span>|-- agent_pool/ (${agents.length})</span>
        <span>|-- runtime/</span>
        <span>\`-- governance/</span>
      </div>
    </article>
  `;
}

function renderProjectExplorer(sections) {
  if (!sections.length) {
    return `<div class="empty-state">暂无项目资源。</div>`;
  }
  return sections
    .map(
      (section) => `
        <article class="explorer-row">
          <div>
            <strong>${escapeHtml(section.name)}</strong>
            <small>${escapeHtml(section.name_zh || "")}</small>
          </div>
          <div class="project-meta">
            <span>${escapeHtml(section.status)}</span>
            <span>${escapeHtml(section.items)} items</span>
          </div>
          <div class="artifact">${escapeHtml(section.path)}</div>
          <p>${escapeHtml(section.description || "")}</p>
        </article>
      `,
    )
    .join("");
}

function renderAgentConsole(agents, bindings, timeline) {
  const hotAgentIds = new Set(timeline.slice(-6).map((item) => item.agent_id));
  const visibleAgents = agents
    .filter((agent) => agent.id !== "KING-XU")
    .sort((a, b) => Number(hotAgentIds.has(b.id)) - Number(hotAgentIds.has(a.id)))
    .slice(0, 8);
  const agentRows = visibleAgents
    .map((agent) => {
      const binding = bindings.find((item) => item.agent_id === agent.id);
      return `
        <article class="console-agent" style="--agent-color:${escapeHtml(agent.accent)}">
          <div class="avatar">${escapeHtml(agent.avatar)}</div>
          <div>
            <strong>${escapeHtml(agent.nickname)}</strong>
            <div class="small">${escapeHtml(agent.role)}</div>
            <div class="small">${escapeHtml(binding?.project_code || "unbound")}</div>
          </div>
          ${statusPill(agent.status)}
        </article>
      `;
    })
    .join("");
  const chatRows = timeline
    .slice(-4)
    .reverse()
    .map(
      (item) => `
        <article class="console-message">
          <strong>${escapeHtml(item.agent || item.agent_id)}</strong>
          <p>${escapeHtml(item.task || "")}</p>
          <small>${escapeHtml(item.provider_id || "")} · ${escapeHtml(item.status || "")}</small>
        </article>
      `,
    )
    .join("");
  return `
    <div class="console-agent-list">${agentRows}</div>
    <div class="console-divider">Conversation Trace <small>最近协作</small></div>
    <div class="console-chat">${chatRows || `<div class="empty-state">暂无 Agent 对话轨迹。</div>`}</div>
  `;
}

function renderExecutionTerminal(terminal) {
  const providerRows = (terminal.provider_calls || [])
    .slice()
    .reverse()
    .map((item) => terminalLine(item.status, item.provider_id, item.task || item.artifact))
    .join("");
  const auditRows = (terminal.audit_logs || [])
    .slice()
    .reverse()
    .map((item) => terminalLine(item.type, item.recorded_by || "audit", item.note || item.recorded_at))
    .join("");
  const worker = terminal.worker_logs?.summary || {};
  const codex = terminal.codex_output;
  return `
    <div class="terminal-grid">
      <div class="terminal-pane">
        <strong>Provider Calls</strong>
        ${providerRows || `<span class="terminal-line">No provider calls</span>`}
      </div>
      <div class="terminal-pane">
        <strong>Audit Logs</strong>
        ${auditRows || `<span class="terminal-line">No audit events</span>`}
      </div>
      <div class="terminal-pane">
        <strong>Worker Logs</strong>
        ${terminalLine("completed", "worker", `${worker.completed || 0} completed / ${worker.rejected || 0} rejected`)}
        ${terminalLine("dry_run", "worker", `${worker.dry_run_pass || 0} dry-run pass`)}
      </div>
      <div class="terminal-pane">
        <strong>Codex Output</strong>
        ${
          codex
            ? terminalLine(codex.status, codex.provider_id, codex.artifact || codex.task)
            : `<span class="terminal-line">No Codex output</span>`
        }
      </div>
    </div>
  `;
}

function terminalLine(status, source, message) {
  return `
    <span class="terminal-line">
      <b>[${escapeHtml(status || "INFO")}]</b>
      <em>${escapeHtml(source || "system")}</em>
      ${escapeHtml(message || "")}
    </span>
  `;
}

function renderAgentPoolSummary(agents) {
  const counts = agents.reduce((acc, agent) => {
    acc[agent.department] = (acc[agent.department] || 0) + 1;
    return acc;
  }, {});
  return `
    <article class="agent-pool-row">
      <strong>公司级共享 Agent Pool</strong>
      <div class="workspace-meta">
        <span>总角色: ${agents.length}</span>
        <span>高管: ${counts.executive || 0}</span>
        <span>专业部门: ${counts.engineering || 0}</span>
        <span>专家组: ${counts.expert || 0}</span>
        <span>审计: ${counts.audit || 0}</span>
      </div>
      <p class="small">Agent 不属于单个项目。绑定 Project Pack 后，才进入该项目上下文。</p>
    </article>
  `;
}

function renderProjects(snapshot) {
  const projects = snapshot.projects || [];
  byId("project-list").innerHTML =
    projects.map((project) => renderProjectRow(project, false)).join("") ||
    `<div class="empty-state">还没有真实项目记忆目录。</div>`;
  renderProjectDrafts(snapshot.project_drafts || []);
}

function renderProjectRow(project, compact) {
  const badge = project.empty_slot ? "空槽位" : project.status === "active" ? "当前项目" : "可打开";
  return `
    <article class="project-row">
      <div class="project-meta">
        <span class="project-badge ${project.empty_slot ? "pending" : ""}">${escapeHtml(badge)}</span>
        <span>${escapeHtml(project.code)}</span>
      </div>
      <strong>${escapeHtml(project.name)}</strong>
      <div class="project-meta">
        <span>记忆文件: ${escapeHtml(project.memory_files ?? 0)}</span>
        <span>${escapeHtml(project.memory_path)}</span>
      </div>
      ${
        compact
          ? ""
          : `<div class="inline-actions">
              <button class="mini-button open-project-row" data-project-code="${escapeHtml(project.code)}">打开<small>查看上下文</small></button>
            </div>`
      }
    </article>
  `;
}

function renderProjectDrafts(drafts) {
  if (!drafts.length) {
    byId("project-draft-list").innerHTML = `<div class="empty-state">暂无新项目申请。这里不会自动创建空项目目录。</div>`;
    return;
  }
  byId("project-draft-list").innerHTML = drafts
    .slice()
    .reverse()
    .map(
      (draft) => `
        <article class="draft-row">
          <div class="draft-meta">
            <span class="project-badge pending">${escapeHtml(draft.status || "DRAFT_RECORDED")}</span>
            <span>${escapeHtml(draft.created_at || "")}</span>
          </div>
          <strong>${escapeHtml(draft.name)} / ${escapeHtml(draft.code)}</strong>
          <div class="draft-meta">
            <span>创建目录: ${draft.creates_project_directory ? "是" : "否"}</span>
            <span>空槽位: ${draft.empty_slot_created ? "已创建" : "未创建"}</span>
            <span>${escapeHtml(draft.note || "")}</span>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderBindings(snapshot) {
  const bindings = snapshot.agent_bindings || [];
  byId("binding-list").innerHTML =
    bindings.map((binding) => renderBindingRow(binding, false)).join("") ||
    `<div class="empty-state">暂无项目绑定。</div>`;
}

function renderBindingRow(binding, compact) {
  return `
    <article class="binding-row">
      <div>
        <strong>${escapeHtml(binding.nickname)}</strong>
        <div class="small">${escapeHtml(binding.agent_id)} · ${escapeHtml(binding.role)}</div>
      </div>
      <div>
        <div class="task-title">${escapeHtml(binding.binding_label)}</div>
        <div class="binding-meta">
          <span>${escapeHtml(binding.project_code)}</span>
          <span>记忆隔离: ${binding.context_isolated ? "是" : "否"}</span>
          ${compact ? "" : `<span>${escapeHtml(binding.memory_scope)}</span>`}
        </div>
      </div>
      ${statusPill(binding.status)}
    </article>
  `;
}

function renderAgents(snapshot) {
  const groups = [
    ["board", "董事会"],
    ["executive", "AI 高管层"],
    ["audit", "审计部门"],
    ["engineering", "专业部门"],
    ["expert", "专家组"],
    ["knowledge", "知识与记忆中心"],
  ];
  byId("org-layout").innerHTML = groups
    .map(([department, title]) => {
      const agents = snapshot.agents.filter((agent) => agent.department === department);
      if (!agents.length) return "";
      return `
        <div>
          <div class="org-group-title">${title}</div>
          <div class="org-row">
            ${agents.map(renderAgentNode).join("")}
          </div>
        </div>
      `;
    })
    .join("");
}

function renderAgentNode(agent) {
  const status = statusClass(agent.status);
  const invocations = agent.metrics?.invocations ?? 0;
  return `
    <article class="agent-node" data-status="${escapeHtml(agent.status)}" style="--agent-color:${escapeHtml(agent.accent)}">
      <div class="avatar">${escapeHtml(agent.avatar)}</div>
      <div>
        <div class="agent-name">
          <strong>${escapeHtml(agent.nickname)}</strong>
          <span class="status-pill ${status}">${escapeHtml(agent.status_label)}<small>${escapeHtml(zhStatus(agent.status) || zhStatus(agent.status_label))}</small></span>
        </div>
        <div class="agent-role">${escapeHtml(agent.role)}</div>
        <div class="agent-id">${escapeHtml(agent.id)} · ${invocations} invocations</div>
        <div class="inline-actions">
          <button class="mini-button agent-trace-button" data-agent-id="${escapeHtml(agent.id)}">日志<small>全过程</small></button>
        </div>
      </div>
    </article>
  `;
}

function renderTasks(snapshot) {
  byId("task-flow").innerHTML = snapshot.tasks
    .map((task) => {
      const status = statusClass(task.status, "task");
      return `
        <article class="task-item">
          <span class="task-status ${status}">${escapeHtml(task.status)}<small>${escapeHtml(zhStatus(task.status))}</small></span>
          <div>
            <div class="task-title">${escapeHtml(task.title)}</div>
            <div class="artifact">${escapeHtml(task.artifact)}</div>
          </div>
          <div class="small">${escapeHtml(agentName(task.assignee))}</div>
          <div>
            <div class="small">${escapeHtml(task.phase)}</div>
            <div class="inline-actions">
              <button class="mini-button start-run-button" data-task-id="${escapeHtml(task.id)}">启动<small>建命令</small></button>
              <button class="mini-button task-trace-button" data-task-id="${escapeHtml(task.id)}">Trace<small>追踪</small></button>
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderTimeline(snapshot) {
  if (!snapshot.timeline.length) {
    byId("timeline").innerHTML = `<div class="empty-state">暂无 Provider 调用轨迹。</div>`;
    return;
  }
  byId("timeline").innerHTML = snapshot.timeline
    .map((item) => {
      const providerStatus = statusClass(item.status, "provider");
      return `
        <article class="timeline-item">
          <div class="timeline-seq">${escapeHtml(item.sequence)}</div>
          <div>
            <div class="timeline-title">${escapeHtml(item.agent)}：${escapeHtml(item.task)}</div>
            <div class="timeline-meta">
              <span>${escapeHtml(item.run_name)}</span>
              <span>${escapeHtml(item.provider_id)}</span>
              <span>${item.mock ? "mock 模拟" : "real 真实"}</span>
              <span>${item.simulated ? "simulated 模拟执行" : "not simulated 非模拟"}</span>
            </div>
            <div class="artifact">${escapeHtml(item.artifact || "")}</div>
          </div>
          <div>
            ${statusPill(item.status, "provider")}
            ${item.codex_version ? `<div class="small">${escapeHtml(item.codex_version)}</div>` : ""}
          </div>
        </article>
      `;
    })
    .join("");
}

function renderQueue(snapshot) {
  if (!snapshot.human_queue.length) {
    byId("human-queue").innerHTML = `<div class="empty-state">当前没有 Human Queue 项。</div>`;
    return;
  }
  byId("human-queue").innerHTML = snapshot.human_queue
    .map((item) => {
      const decided = item.dashboard_decision;
      return `
        <article class="queue-row">
          <div>
            <div class="task-title">${escapeHtml(item.task)}</div>
            <div class="artifact">${escapeHtml(item.reason)}</div>
          </div>
          <div>
            <div class="small">申请人</div>
            <strong>${escapeHtml(agentName(item.requester))}</strong>
          </div>
          <div>
            <span class="status-pill status-human">${escapeHtml(decided?.decision || item.queue_status)}</span>
            <div class="small">${escapeHtml(item.approver)}</div>
          </div>
          <div class="queue-actions">
            <button class="action-button action-approve" data-decision="approve" data-key="${escapeHtml(item.item_key)}">批准<small>同意记录</small></button>
            <button class="action-button action-reject" data-decision="reject" data-key="${escapeHtml(item.item_key)}">拒绝<small>阻断记录</small></button>
            <button class="action-button action-return" data-decision="return" data-key="${escapeHtml(item.item_key)}">打回<small>退回修改</small></button>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderCommandLog(snapshot) {
  const commands = snapshot.commands || [];
  if (!commands.length) {
    return `<div class="empty-state">暂无 Dashboard 命令。</div>`;
  }
  return commands
    .slice()
    .reverse()
    .map(renderCommandCard)
    .join("");
}

function renderMetrics(snapshot) {
  if (!snapshot.metrics.length) {
    byId("metrics").innerHTML = `<div class="empty-state">暂无 metrics 文件。</div>`;
    return;
  }
  byId("metrics").innerHTML = snapshot.metrics
    .map((metric) => {
      const rate = Math.round((metric.provider_success_rate || 0) * 100);
      return `
        <article class="metric-item">
          <h3>${escapeHtml(agentName(metric.agent_id))} · ${escapeHtml(metric.agent_id)}</h3>
          <div class="metric-line">${term("Runs")}<strong>${metric.runs ?? 0}</strong></div>
          <div class="metric-line">${term("Invocations")}<strong>${metric.invocations ?? 0}</strong></div>
          <div class="metric-line">${term("Provider Executed")}<strong>${metric.provider_executed ?? 0}</strong></div>
          <div class="metric-line">${term("Approval Requests")}<strong>${metric.approval_requests ?? 0}</strong></div>
          <div class="bar-track"><div class="bar-fill" style="width:${rate}%"></div></div>
          <div class="small">Provider success · Provider成功率 ${rate}%</div>
        </article>
      `;
    })
    .join("");
}

function renderProviders(snapshot) {
  byId("providers").innerHTML = snapshot.providers
    .map((provider) => {
      const status = provider.last_status || provider.status;
      const providerStatus = statusClass(status, "provider");
      const caps = provider.capabilities || [];
      return `
        <article class="provider-item">
          <div class="provider-name">
            <strong>${escapeHtml(provider.name)}</strong>
            ${statusPill(status, "provider")}
          </div>
          <div class="small">${escapeHtml(provider.id)} · ${escapeHtml(provider.execution_mode)}</div>
          <div class="small">Last: ${escapeHtml(provider.last_task || "no invocation yet")}</div>
          <div class="provider-caps">
            ${caps.slice(0, 5).map((cap) => `<span class="cap">${escapeHtml(cap)}</span>`).join("")}
          </div>
        </article>
      `;
    })
    .join("");
}

function snapshotSignature(snapshot) {
  return JSON.stringify({
    workspace: snapshot.workspace,
    projects: snapshot.projects?.map((project) => [
      project.code,
      project.status,
      project.memory_files,
    ]),
    projectDrafts: snapshot.project_drafts?.map((draft) => [
      draft.draft_id,
      draft.status,
    ]),
    bindings: snapshot.agent_bindings?.map((binding) => [
      binding.agent_id,
      binding.project_code,
      binding.status,
    ]),
    explorer: snapshot.project_explorer?.map((section) => [
      section.id,
      section.items,
      section.status,
    ]),
    terminal: {
      providers: snapshot.execution_terminal?.provider_calls?.length || 0,
      audits: snapshot.execution_terminal?.audit_logs?.length || 0,
      codex: snapshot.execution_terminal?.codex_output?.id || "",
    },
    agents: snapshot.agents.map((agent) => [agent.id, agent.status, agent.metrics?.invocations ?? 0]),
    tasks: snapshot.tasks.map((task) => [task.id, task.status, task.last_command?.command_id || ""]),
    queue: snapshot.human_queue.map((item) => [
      item.item_key,
      item.queue_status,
      item.dashboard_decision?.decision || "",
    ]),
    metrics: snapshot.metrics.map((metric) => [metric.agent_id, metric.last_updated]),
    providers: snapshot.providers.map((provider) => [
      provider.id,
      provider.status,
      provider.last_status || "",
    ]),
    timeline: snapshot.timeline.length,
    commands:
      snapshot.commands?.map((command) => [
        command.command_id,
        command.status,
        command.events?.length || 0,
      ]) || [],
    worker: snapshot.worker_summary?.last_event || null,
  });
}

function render(snapshot) {
  const signature = snapshotSignature(snapshot);
  state.snapshot = snapshot;
  byId("project-title").textContent = snapshot.project.name;
  byId("runtime-label").textContent = snapshot.project.runtime_baseline;
  byId("updated-at").textContent = snapshot.generated_at;
  if (signature === state.lastSignature) return;
  state.lastSignature = signature;
  renderSummary(snapshot);
  renderWorkspace(snapshot);
  renderProjects(snapshot);
  renderBindings(snapshot);
  renderAgents(snapshot);
  renderTasks(snapshot);
  renderTimeline(snapshot);
  renderQueue(snapshot);
  renderMetrics(snapshot);
  renderProviders(snapshot);
}

async function loadSnapshot() {
  const response = await fetch("/api/snapshot");
  render(await response.json());
}

function switchView(view) {
  state.activeView = view;
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.remove("active"));
  const panel = byId(`view-${view}`);
  if (panel) panel.classList.add("active");
}

async function recordProjectDraft() {
  const nameInput = byId("new-project-name");
  const codeInput = byId("new-project-code");
  const name = nameInput.value.trim();
  const code = codeInput.value.trim();
  if (!name || !code) {
    showDetail("New Project", "请先填写项目名称和项目代号", `
      <div class="empty-state">Alpha 阶段不会创建空项目目录。请填写名称和代号后，只记录一条新项目申请。</div>
    `);
    return;
  }
  const response = await fetch("/api/projects/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      code,
      note: "Recorded from OMC-OS Workbench Alpha UI",
    }),
  });
  if (!response.ok) throw new Error("project draft failed");
  const result = await response.json();
  nameInput.value = "";
  codeInput.value = "";
  await loadSnapshot();
  showDetail("New Project", "新项目申请已记录，不创建空目录", `
    <article class="draft-row">
      <strong>${escapeHtml(result.draft.name)} / ${escapeHtml(result.draft.code)}</strong>
      <div class="draft-meta">
        <span>${escapeHtml(result.draft.status)}</span>
        <span>创建目录: ${result.draft.creates_project_directory ? "是" : "否"}</span>
        <span>空槽位: ${result.draft.empty_slot_created ? "已创建" : "未创建"}</span>
      </div>
      <p class="small">${escapeHtml(result.draft.blocked_reason)}</p>
    </article>
  `);
}

function showProjectContext(projectCode) {
  const project = state.snapshot?.projects?.find((item) => item.code === projectCode);
  if (!project) return;
  showDetail("Project Context", `${project.name} 项目上下文`, `
    ${renderProjectRow(project, true)}
    <div class="empty-state">当前 Alpha 只打开项目上下文视图。后续“打开项目”会切换 Project Pack、Memory、Tasks、Outputs、Audit 五个目录。</div>
  `);
}

function showImportMaterialsPlaceholder() {
  showDetail("Import Materials", "导入资料入口尚处于安全占位", `
    <div class="empty-state">
      这一版不会自动读写外部资料。下一步可以做“选择资料 -> 生成导入清单 -> King Xu 确认 -> 写入 Project Pack”的安全流程。
    </div>
  `);
}

async function startRun(taskId = "NEXT-001") {
  const task = state.snapshot?.tasks?.find((item) => item.id === taskId);
  const response = await fetch("/api/runs/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project: state.snapshot?.project?.name,
      task_id: taskId,
      agent_id: task?.assignee,
      title: task?.title,
      note: "Requested from Command Center Alpha UI",
    }),
  });
  if (!response.ok) throw new Error("run start failed");
  const result = await response.json();
  await loadSnapshot();
  showDetail("Command", "启动请求已创建", `
    ${renderCommandCard(result.command)}
  `);
}

function connectSocket() {
  const dot = byId("socket-dot");
  const label = byId("socket-label");
  const protocol = location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${protocol}://${location.host}/ws`);
  socket.addEventListener("open", () => {
    dot.className = "status-dot connected";
    label.textContent = "Live";
  });
  socket.addEventListener("message", (event) => {
    render(JSON.parse(event.data));
  });
  socket.addEventListener("close", () => {
    dot.className = "status-dot disconnected";
    label.textContent = "Polling";
    setTimeout(connectSocket, 3000);
  });
  socket.addEventListener("error", () => {
    socket.close();
  });
}

async function recordDecision(itemKey, decision) {
  const encoded = encodeURIComponent(itemKey);
  if (decision === "approve" || decision === "reject") {
    await fetch(`/api/human-queue/${encoded}/${decision}`, { method: "POST" });
  } else {
    await fetch(`/api/human-queue/${encoded}/decision`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision, note: "Returned from Command Center Alpha UI" }),
    });
  }
  await loadSnapshot();
}

async function showAgentTrace(agentId) {
  const response = await fetch(`/api/agents/${encodeURIComponent(agentId)}/timeline`);
  if (!response.ok) throw new Error("agent trace failed");
  const trace = await response.json();
  const body = [
    renderTraceSummary(trace.agent.nickname, trace.agent.role, trace.metrics),
    renderTraceEvents(trace.timeline, "该角色暂无 Provider 调用记录。"),
    renderTraceCommands(trace.commands),
  ].join("");
  showDetail("Agent Timeline", `${trace.agent.nickname} 全过程日志`, body);
}

async function showTaskTrace(taskId) {
  const response = await fetch(`/api/tasks/${encodeURIComponent(taskId)}/trace`);
  if (!response.ok) throw new Error("task trace failed");
  const trace = await response.json();
  const assignee = trace.assignee?.nickname || trace.task.assignee;
  const body = [
    renderTaskSummary(trace.task, assignee, trace.artifact_exists),
    renderTraceEvents(trace.timeline, "该任务暂无直接调用记录。"),
    renderTraceCommands(trace.commands),
  ].join("");
  showDetail("Task Trace", `${trace.task.title} 执行链`, body);
}

function renderTraceSummary(title, subtitle, metrics = {}) {
  return `
    <div class="trace-summary">
      <div>
        <span class="meta-label">Target <small>对象</small></span>
        <strong>${escapeHtml(title)}</strong>
      </div>
      <div>
        <span class="meta-label">Role <small>角色</small></span>
        <strong>${escapeHtml(subtitle)}</strong>
      </div>
      <div>
        <span class="meta-label">Invocations <small>调用次数</small></span>
        <strong>${escapeHtml(metrics.invocations ?? 0)}</strong>
      </div>
    </div>
  `;
}

function renderTaskSummary(task, assignee, artifactExists) {
  return `
    <div class="trace-summary">
      <div>
        <span class="meta-label">Task <small>任务</small></span>
        <strong>${escapeHtml(task.id)}</strong>
      </div>
      <div>
        <span class="meta-label">Assignee <small>负责人</small></span>
        <strong>${escapeHtml(assignee)}</strong>
      </div>
      <div>
        <span class="meta-label">Artifact <small>产物</small></span>
        <strong>${artifactExists ? "exists" : "pending"}</strong>
      </div>
    </div>
    <div class="artifact">${escapeHtml(task.artifact)}</div>
  `;
}

function renderTraceEvents(events, emptyText) {
  if (!events.length) return `<div class="empty-state">${escapeHtml(emptyText)}</div>`;
  return events
    .map(
      (item) => `
        <article class="trace-row">
          <div>
            <strong>${escapeHtml(item.task)}</strong>
            <div class="artifact">${escapeHtml(item.artifact || "")}</div>
          </div>
          <div class="small">${escapeHtml(item.run_name)} · ${escapeHtml(item.provider_id)}</div>
          ${statusPill(item.status, "provider")}
        </article>
      `,
    )
    .join("");
}

function renderTraceCommands(commands) {
  if (!commands.length) return `<div class="empty-state">暂无 Dashboard 命令记录。</div>`;
  return commands
    .slice()
    .reverse()
    .map(renderCommandCard)
    .join("");
}

function renderCommandCard(command) {
  return `
    <article class="command-card">
      <div class="command-main">
        <div>
          <strong>${escapeHtml(command.task_title)}</strong>
          <div class="artifact">${escapeHtml(command.command_id)}</div>
        </div>
        ${statusPill(command.status, "provider")}
      </div>
      <div class="command-meta">
        <span>${escapeHtml(command.agent)}</span>
        <span>${escapeHtml(command.dry_run?.task_type || "unknown")} · ${escapeHtml(TERM_ZH[command.dry_run?.task_type] || "任务类型")}</span>
        <span>risk 风险: ${escapeHtml(command.dry_run?.risk || "unknown")} · ${escapeHtml(TERM_ZH[command.dry_run?.risk] || "")}</span>
        <span>${escapeHtml(command.created_at)}</span>
      </div>
      <div class="gate-row">${renderGateChips(command)}</div>
      <div class="command-actions">${renderCommandActions(command)}</div>
    </article>
  `;
}

function renderGateChips(command) {
  const gates = command.gates || [];
  if (!gates.length) return `<span class="gate-chip gate-waiting">No gates<small>暂无门禁</small></span>`;
  return gates
    .map((gate) => {
      const passed = gate.status === "PASS";
      return `<span class="gate-chip ${passed ? "gate-pass" : "gate-waiting"}">${escapeHtml(gate.label)} · ${escapeHtml(gate.status)}<small>${passed ? "已通过" : "等待处理"}</small></span>`;
    })
    .join("");
}

function renderCommandActions(command) {
  const buttons = [
    `<button class="mini-button command-action-button" data-command-action="dry-run" data-command-id="${escapeHtml(command.command_id)}">Dry Run<small>试跑</small></button>`,
  ];
  const missing = command.missing_gates || [];
  if (command.status === "REJECTED") {
    buttons.push(`<span class="gate-chip gate-blocked">已拒绝</span>`);
    return buttons.join("");
  }
  if (missing.includes("production_whitelist")) {
    buttons.push(`<span class="gate-chip gate-blocked">生产默认禁止，需手动白名单</span>`);
  } else if (missing.includes("human_approval")) {
    buttons.push(
      `<button class="mini-button command-action-button" data-command-action="approve" data-command-id="${escapeHtml(command.command_id)}">King Xu 批准<small>人工同意</small></button>`,
      `<button class="mini-button command-action-button" data-command-action="reject" data-command-id="${escapeHtml(command.command_id)}">拒绝<small>阻断任务</small></button>`,
    );
  } else if (missing.includes("audit_pass")) {
    buttons.push(
      `<button class="mini-button command-action-button" data-command-action="audit-pass" data-command-id="${escapeHtml(command.command_id)}">赵云审计通过<small>允许继续</small></button>`,
    );
  } else if (command.safe_execution?.can_execute) {
    buttons.push(
      `<button class="primary-button command-action-button" data-command-action="execute" data-command-id="${escapeHtml(command.command_id)}">安全执行<small>进入队列</small></button>`,
    );
  }
  if (command.status === "SAFE_EXECUTION_QUEUED") {
    buttons.push(
      `<span class="gate-chip gate-pass">已进入 Safe Execution Queue</span>`,
      `<button class="mini-button command-action-button" data-command-action="worker-dry-run" data-command-id="${escapeHtml(command.command_id)}">Worker Dry Run<small>工人试跑</small></button>`,
      `<button class="primary-button command-action-button" data-command-action="worker-execute" data-command-id="${escapeHtml(command.command_id)}">Worker 执行<small>低风险闭环</small></button>`,
    );
  }
  if (command.status === "WORKER_COMPLETED") {
    buttons.push(`<span class="gate-chip gate-pass">Worker 已完成</span>`);
  }
  if (command.status === "WORKER_FAILED" || command.status === "WORKER_REJECTED") {
    buttons.push(`<span class="gate-chip gate-blocked">${escapeHtml(command.status)}</span>`);
  }
  return buttons.join("");
}

async function commandAction(commandId, action) {
  if (action === "worker-dry-run" || action === "worker-execute") {
    return workerRun(commandId, action === "worker-dry-run");
  }
  const response = await fetch(`/api/commands/${encodeURIComponent(commandId)}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note: "Recorded from Command Center Safe Execution UI" }),
  });
  if (!response.ok) throw new Error("command action failed");
  const result = await response.json();
  await loadSnapshot();
  showDetail("Safe Execution", "门禁状态已更新", renderCommandCard(result.command));
}

async function workerRun(commandId, dryRun) {
  const response = await fetch("/api/worker/run-once", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      command_id: commandId,
      dry_run: dryRun,
      limit: 1,
      timeout_seconds: 300,
    }),
  });
  if (!response.ok) throw new Error("worker run failed");
  const result = await response.json();
  await loadSnapshot();
  const rows = result.worker.results
    .map(
      (item) => `
        <article class="trace-row">
          <div>
            <strong>${escapeHtml(item.status)}</strong>
            <div class="artifact">${escapeHtml(item.output_dir || item.reasons?.join("; ") || "")}</div>
          </div>
          <div class="small">${escapeHtml(item.provider_status || "")}</div>
          <span class="status-pill ${item.status === "WORKER_COMPLETED" ? "status-complete" : "status-waiting"}">${dryRun ? "Dry Run" : "Worker"}<small>${dryRun ? "试跑" : "执行"}</small></span>
        </article>
      `,
    )
    .join("");
  showDetail("Safe Execution Worker", dryRun ? "Worker Dry Run" : "Worker 执行结果", rows || `<div class="empty-state">Worker 没有可处理命令。</div>`);
}

function showDetail(kicker, title, body) {
  byId("detail-kicker").textContent = kicker;
  byId("detail-title").textContent = title;
  byId("detail-body").innerHTML = body;
  byId("detail-panel").classList.add("active");
  byId("detail-panel").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

document.addEventListener("click", (event) => {
  const navButton = event.target.closest(".nav-button");
  if (navButton) {
    switchView(navButton.dataset.view);
    return;
  }

  const action = event.target.closest(".action-button");
  if (action) {
    recordDecision(action.dataset.key, action.dataset.decision).catch(() => {
      byId("socket-label").textContent = "Decision failed";
    });
    return;
  }

  const startButton = event.target.closest(".start-run-button");
  if (startButton) {
    startRun(startButton.dataset.taskId).catch(() => {
      byId("socket-label").textContent = "Start failed";
    });
    return;
  }

  const agentTrace = event.target.closest(".agent-trace-button");
  if (agentTrace) {
    showAgentTrace(agentTrace.dataset.agentId).catch(() => {
      byId("socket-label").textContent = "Trace failed";
    });
    return;
  }

  const taskTrace = event.target.closest(".task-trace-button");
  if (taskTrace) {
    showTaskTrace(taskTrace.dataset.taskId).catch(() => {
      byId("socket-label").textContent = "Trace failed";
    });
    return;
  }

  const commandActionButton = event.target.closest(".command-action-button");
  if (commandActionButton) {
    commandAction(commandActionButton.dataset.commandId, commandActionButton.dataset.commandAction).catch(() => {
      byId("socket-label").textContent = "Gate action failed";
    });
    return;
  }

  if (event.target.closest("#record-project-draft")) {
    recordProjectDraft().catch(() => {
      byId("socket-label").textContent = "Project draft failed";
    });
    return;
  }

  const openProject = event.target.closest(".open-project-row");
  if (openProject) {
    showProjectContext(openProject.dataset.projectCode);
    return;
  }

  if (event.target.closest("#open-active-project")) {
    switchView("projects");
    return;
  }

  if (event.target.closest("#import-materials-request")) {
    showImportMaterialsPlaceholder();
    return;
  }

  if (event.target.closest("#start-next-run")) {
    startRun("NEXT-001").catch(() => {
      byId("socket-label").textContent = "Start failed";
    });
    return;
  }

  if (event.target.closest("#open-command-log")) {
    showDetail("Command Log", "Dashboard 命令日志", renderCommandLog(state.snapshot));
    return;
  }

  if (event.target.closest("#close-detail")) {
    byId("detail-panel").classList.remove("active");
  }
});

loadSnapshot().catch(() => {
  byId("socket-label").textContent = "Snapshot failed";
});
connectSocket();
setInterval(loadSnapshot, 10000);
