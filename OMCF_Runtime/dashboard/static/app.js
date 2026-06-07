const state = {
  snapshot: null,
  activeView: "agents",
  lastSignature: "",
};

const statusClass = (value, prefix = "status") =>
  `${prefix}-${String(value || "idle").toLowerCase().replaceAll(" ", "_")}`;

const byId = (id) => document.getElementById(id);

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

function renderSummary(snapshot) {
  const running = snapshot.agents.filter((agent) => agent.status === "running").length;
  const queue = snapshot.human_queue.filter((item) => item.queue_status === "pending").length;
  const commands = snapshot.commands?.length || 0;
  const safeReady = snapshot.safe_execution_summary?.ready || 0;
  const safeQueued = snapshot.safe_execution_summary?.queued || 0;
  byId("summary-grid").innerHTML = `
    <div class="summary-item"><span>Running Agents</span><strong>${running}</strong></div>
    <div class="summary-item"><span>Safe Ready</span><strong>${safeReady}</strong></div>
    <div class="summary-item"><span>Human Queue</span><strong>${queue}</strong></div>
    <div class="summary-item"><span>Commands / Queue</span><strong>${commands}/${safeQueued}</strong></div>
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
          <span class="status-pill ${status}">${escapeHtml(agent.status_label)}</span>
        </div>
        <div class="agent-role">${escapeHtml(agent.role)}</div>
        <div class="agent-id">${escapeHtml(agent.id)} · ${invocations} invocations</div>
        <div class="inline-actions">
          <button class="mini-button agent-trace-button" data-agent-id="${escapeHtml(agent.id)}">日志</button>
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
          <span class="task-status ${status}">${escapeHtml(task.status)}</span>
          <div>
            <div class="task-title">${escapeHtml(task.title)}</div>
            <div class="artifact">${escapeHtml(task.artifact)}</div>
          </div>
          <div class="small">${escapeHtml(agentName(task.assignee))}</div>
          <div>
            <div class="small">${escapeHtml(task.phase)}</div>
            <div class="inline-actions">
              <button class="mini-button start-run-button" data-task-id="${escapeHtml(task.id)}">启动</button>
              <button class="mini-button task-trace-button" data-task-id="${escapeHtml(task.id)}">Trace</button>
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
              <span>${item.mock ? "mock" : "real"}</span>
              <span>${item.simulated ? "simulated" : "not simulated"}</span>
            </div>
            <div class="artifact">${escapeHtml(item.artifact || "")}</div>
          </div>
          <div>
            <span class="provider-status ${providerStatus}">${escapeHtml(item.status)}</span>
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
            <button class="action-button action-approve" data-decision="approve" data-key="${escapeHtml(item.item_key)}">批准</button>
            <button class="action-button action-reject" data-decision="reject" data-key="${escapeHtml(item.item_key)}">拒绝</button>
            <button class="action-button action-return" data-decision="return" data-key="${escapeHtml(item.item_key)}">打回</button>
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
          <div class="metric-line"><span>Runs</span><strong>${metric.runs ?? 0}</strong></div>
          <div class="metric-line"><span>Invocations</span><strong>${metric.invocations ?? 0}</strong></div>
          <div class="metric-line"><span>Provider Executed</span><strong>${metric.provider_executed ?? 0}</strong></div>
          <div class="metric-line"><span>Approval Requests</span><strong>${metric.approval_requests ?? 0}</strong></div>
          <div class="bar-track"><div class="bar-fill" style="width:${rate}%"></div></div>
          <div class="small">Provider success ${rate}%</div>
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
            <span class="provider-status ${providerStatus}">${escapeHtml(status)}</span>
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
        <span class="meta-label">Target</span>
        <strong>${escapeHtml(title)}</strong>
      </div>
      <div>
        <span class="meta-label">Role</span>
        <strong>${escapeHtml(subtitle)}</strong>
      </div>
      <div>
        <span class="meta-label">Invocations</span>
        <strong>${escapeHtml(metrics.invocations ?? 0)}</strong>
      </div>
    </div>
  `;
}

function renderTaskSummary(task, assignee, artifactExists) {
  return `
    <div class="trace-summary">
      <div>
        <span class="meta-label">Task</span>
        <strong>${escapeHtml(task.id)}</strong>
      </div>
      <div>
        <span class="meta-label">Assignee</span>
        <strong>${escapeHtml(assignee)}</strong>
      </div>
      <div>
        <span class="meta-label">Artifact</span>
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
          <span class="provider-status ${statusClass(item.status, "provider")}">${escapeHtml(item.status)}</span>
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
        <span class="provider-status ${statusClass(command.status, "provider")}">${escapeHtml(command.status)}</span>
      </div>
      <div class="command-meta">
        <span>${escapeHtml(command.agent)}</span>
        <span>${escapeHtml(command.dry_run?.task_type || "unknown")}</span>
        <span>risk: ${escapeHtml(command.dry_run?.risk || "unknown")}</span>
        <span>${escapeHtml(command.created_at)}</span>
      </div>
      <div class="gate-row">${renderGateChips(command)}</div>
      <div class="command-actions">${renderCommandActions(command)}</div>
    </article>
  `;
}

function renderGateChips(command) {
  const gates = command.gates || [];
  if (!gates.length) return `<span class="gate-chip gate-waiting">No gates</span>`;
  return gates
    .map((gate) => {
      const passed = gate.status === "PASS";
      return `<span class="gate-chip ${passed ? "gate-pass" : "gate-waiting"}">${escapeHtml(gate.label)} · ${escapeHtml(gate.status)}</span>`;
    })
    .join("");
}

function renderCommandActions(command) {
  const buttons = [
    `<button class="mini-button command-action-button" data-command-action="dry-run" data-command-id="${escapeHtml(command.command_id)}">Dry Run</button>`,
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
      `<button class="mini-button command-action-button" data-command-action="approve" data-command-id="${escapeHtml(command.command_id)}">King Xu 批准</button>`,
      `<button class="mini-button command-action-button" data-command-action="reject" data-command-id="${escapeHtml(command.command_id)}">拒绝</button>`,
    );
  } else if (missing.includes("audit_pass")) {
    buttons.push(
      `<button class="mini-button command-action-button" data-command-action="audit-pass" data-command-id="${escapeHtml(command.command_id)}">赵云审计通过</button>`,
    );
  } else if (command.safe_execution?.can_execute) {
    buttons.push(
      `<button class="primary-button command-action-button" data-command-action="execute" data-command-id="${escapeHtml(command.command_id)}">安全执行</button>`,
    );
  }
  if (command.status === "SAFE_EXECUTION_QUEUED") {
    buttons.push(`<span class="gate-chip gate-pass">已进入 Safe Execution Queue</span>`);
  }
  return buttons.join("");
}

async function commandAction(commandId, action) {
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
    state.activeView = navButton.dataset.view;
    document.querySelectorAll(".nav-button").forEach((button) => button.classList.remove("active"));
    navButton.classList.add("active");
    document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.remove("active"));
    byId(`view-${state.activeView}`).classList.add("active");
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
