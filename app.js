(function () {
  const STORAGE_KEY = "ateam-plan-checklist-v1";

  function loadChecked() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveChecked(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  const checked = loadChecked();

  function el(tag, opts) {
    const node = document.createElement(tag);
    opts = opts || {};
    if (opts.text) node.textContent = opts.text;
    if (opts.html) node.innerHTML = opts.html;
    if (opts.class) node.className = opts.class;
    return node;
  }

  function statusClass(status) {
    const s = status.toLowerCase();
    if (s === "live") return "status-live";
    if (s.includes("fix") || s.includes("wrong")) return "status-fix";
    if (s.includes("progress") || s.includes("confirm")) return "status-progress";
    return "status-build";
  }

  function renderHero(meta) {
    document.getElementById("hero-company").textContent = meta.company.toUpperCase();
    document.getElementById("hero-subtitle").textContent = meta.subtitle;
    document.getElementById("hero-tagline").textContent = meta.tagline;
    document.getElementById("hero-meta").textContent =
      meta.preparedFor + " · " + meta.location + " · " + meta.contact;
    document.getElementById("hero-quote").textContent = meta.quote;
    document.getElementById("footer-quote").textContent = meta.quote;
  }

  function renderMission(mission) {
    const list = document.getElementById("mission-list");
    mission.forEach((m) => list.appendChild(el("li", { text: m })));
  }

  function renderChecklist(containerId, items, keyPrefix, progressFillId, progressLabelId) {
    const container = document.getElementById(containerId);
    let doneCount = 0;

    items.forEach((text, i) => {
      const key = keyPrefix + "-" + i;
      const isChecked = !!checked[key];
      if (isChecked) doneCount++;

      const li = el("li", { class: isChecked ? "checked" : "" });
      const cb = el("input");
      cb.type = "checkbox";
      cb.checked = isChecked;
      cb.addEventListener("change", () => {
        checked[key] = cb.checked;
        saveChecked(checked);
        li.classList.toggle("checked", cb.checked);
        updateProgress();
      });
      const span = el("span", { text: text });
      li.appendChild(cb);
      li.appendChild(span);
      container.appendChild(li);
    });

    function updateProgress() {
      if (!progressFillId) return;
      const total = items.length;
      const done = items.reduce(
        (acc, _, i) => acc + (checked[keyPrefix + "-" + i] ? 1 : 0),
        0
      );
      const pct = total ? Math.round((done / total) * 100) : 0;
      document.getElementById(progressFillId).style.width = pct + "%";
      document.getElementById(progressLabelId).textContent =
        done + " of " + total + " done (" + pct + "%)";
    }

    updateProgress();
  }

  function renderLadder(ladder) {
    const container = document.getElementById("ladder-list");
    ladder.forEach((rung) => {
      const div = el("div", { class: "rung" });
      div.appendChild(el("h3", { text: rung.rung }));
      div.appendChild(el("p", { text: rung.desc }));
      container.appendChild(div);
    });
  }

  function renderList(id, items) {
    const container = document.getElementById(id);
    items.forEach((item) => container.appendChild(el("li", { text: item })));
  }

  function renderTable(id, tableData) {
    const table = document.getElementById(id);
    const thead = el("thead");
    const headRow = el("tr");
    tableData.headers.forEach((h) => headRow.appendChild(el("th", { text: h })));
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = el("tbody");
    tableData.rows.forEach((row) => {
      const tr = el("tr");
      row.forEach((cell, idx) => {
        const td = el("td");
        const isLastCol = idx === row.length - 1;
        const looksLikeStatus =
          isLastCol &&
          tableData.headers[idx] &&
          tableData.headers[idx].toLowerCase() === "status";
        if (looksLikeStatus) {
          const pill = el("span", { text: cell, class: "status-pill " + statusClass(cell) });
          td.appendChild(pill);
        } else {
          td.textContent = cell;
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
  }

  function dayNumber(startDateStr) {
    const start = new Date(startDateStr + "T00:00:00");
    const now = new Date();
    const nowMid = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const startMid = new Date(start.getFullYear(), start.getMonth(), start.getDate());
    const diffMs = nowMid - startMid;
    return Math.floor(diffMs / 86400000) + 1; // Day 1 == start date
  }

  function renderPhaseBanner(meta, timeline) {
    const day = dayNumber(meta.startDate);
    const clampedDay = Math.max(1, Math.min(day, 90));
    const active =
      timeline.find((p) => day >= p.startDay && day <= p.endDay) ||
      (day > 90 ? timeline[timeline.length - 1] : timeline[0]);

    document.getElementById("phase-name").textContent = active.phase;
    document.getElementById("phase-day").textContent =
      day < 1 ? "Starts " + meta.startDate : day > 90 ? "Day " + day + " (past Day 90)" : "Day " + day + " of 90";

    let daysLeftText = "";
    if (day < 1) {
      daysLeftText = "Not started yet";
    } else if (day > 90) {
      daysLeftText = "90-day window complete";
    } else {
      daysLeftText = active.endDay - day + " day(s) left in this phase";
    }
    document.getElementById("phase-days-left").textContent = daysLeftText;
  }

  function renderTimeline(timeline, meta) {
    const day = dayNumber(meta.startDate);
    const container = document.getElementById("timeline-list");
    timeline.forEach((phase, pIdx) => {
      const isActive = day >= phase.startDay && day <= phase.endDay;
      const block = el("div", { class: "phase-block" + (isActive ? " active" : "") });
      block.appendChild(el("h3", { text: phase.phase }));
      const ul = el("ul", { class: "checklist" });
      block.appendChild(ul);
      container.appendChild(block);
      phase.items.forEach((text, i) => {
        const key = "phase-" + pIdx + "-" + i;
        const isChecked = !!checked[key];
        const li = el("li", { class: isChecked ? "checked" : "" });
        const cb = el("input");
        cb.type = "checkbox";
        cb.checked = isChecked;
        cb.addEventListener("change", () => {
          checked[key] = cb.checked;
          saveChecked(checked);
          li.classList.toggle("checked", cb.checked);
        });
        const span = el("span", { text: text });
        li.appendChild(cb);
        li.appendChild(span);
        ul.appendChild(li);
      });
    });
  }

  function init() {
    renderHero(PLAN.meta);
    renderMission(PLAN.mission);
    renderChecklist(
      "week-checklist",
      PLAN.doThisWeek,
      "week",
      "week-progress-fill",
      "week-progress-label"
    );
    renderLadder(PLAN.offerLadder);
    renderList("state-working", PLAN.currentState.working);
    renderList("state-broken", PLAN.currentState.broken);
    renderList("state-inprogress", PLAN.currentState.inProgress);
    renderTable("workflow-table", PLAN.workflowTable);
    renderTable("automation-table", PLAN.automationTable);
    renderPhaseBanner(PLAN.meta, PLAN.timeline);
    renderTimeline(PLAN.timeline, PLAN.meta);
    renderTable("kpi-table", PLAN.kpiTable);
    renderList("risks-list", PLAN.risks);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
