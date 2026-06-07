const state = {
  snapshot: null,
  activeView: "agents",
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
  const providers = snapshot.providers.filter((provider) => provider.enabled).length;
  const completion = Math.round(snapshot.task_summary.completion_rate * 100);
  byId("summary-grid").innerHTML = `
    <div class="summary-item"><span>Running Agents</span><strong>${running}</strong></div>
    <div class="summary-item"><span>Task Completion</span><strong>${completion}%</strong></div>
    <div class="summary-item"><span>Human Queue</span><strong>${queue}</strong></div>
    <div class="summary-item"><span>Enabled Providers</span><strong>${providers}</strong></div>
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
          <div class="small">${escapeHtml(task.phase)}</div>
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

function render(snapshot) {
  state.snapshot = snapshot;
  byId("project-title").textContent = snapshot.project.name;
  byId("runtime-label").textContent = snapshot.project.runtime_baseline;
  byId("updated-at").textContent = snapshot.generated_at;
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
  await fetch(`/api/human-queue/${encodeURIComponent(itemKey)}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, note: "Recorded from Dashboard Alpha UI" }),
  });
  await loadSnapshot();
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
  }
});

loadSnapshot().catch(() => {
  byId("socket-label").textContent = "Snapshot failed";
});
connectSocket();
setInterval(loadSnapshot, 10000);
