# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A-Team Contracting's "90-Day Plan Dashboard" — a static, no-backend, no-build, zero-dependency dashboard built with plain HTML/CSS/JS. There is no `package.json`, bundler, framework, linter, test framework, or CI config in this repo.

## Running locally / Deploying

No build step. Either open `index.html` directly in a browser, or serve it:

```
python3 -m http.server 8000
```

Deployed via Netlify (`netlify.toml`): `publish = "."`, no build command — the repo root is served as-is.

## Architecture

The repo is a strict data/render split across three files, loaded in this order from `index.html`:

- **`plan-data.js`** — the only content layer: a global `PLAN` object (`meta`, `mission`, `offerLadder`, `currentState`, `workflowTable`, `automationTable`, `timeline`, `kpiTable`, `risks`, `doThisWeek`).
- **`app.js`** — the rendering engine (an IIFE). On `DOMContentLoaded`, `init()` calls `renderHero`, `renderMission`, `renderChecklist`, `renderLadder`, `renderList`, `renderTable`, `renderPhaseBanner`, and `renderTimeline` in sequence. Each reads its section from `PLAN.*` and writes into a pre-existing empty container in `index.html`, matched by `id`. DOM nodes are built directly (`document.createElement`/`appendChild` via a small `el()` helper) — no virtual DOM.
- **`index.html`** — the page skeleton: empty containers (by `id`) for every section, plus the `<script>` tags loading `plan-data.js` then `app.js`.
- **`styles.css`** — the brand system: colors (Orange `#F58220`, Blue `#1B5B98`, Charcoal `#333333`), fonts (Anton for headlines, Montserrat for body, Caveat for accent).
- **`netlify.toml`** — deploy config only.

## Conventions

- **Content changes belong only in `plan-data.js`.** `app.js` and `index.html` are the stable rendering engine and should not need to change for content edits.
- **Active phase logic**: `PLAN.meta.startDate` drives which of the four 90-day timeline phases is shown as "active," computed by `dayNumber()`/`renderPhaseBanner()` in `app.js`.
- **Checklist persistence**: check-state for `doThisWeek` items and timeline-phase items is persisted client-side only, via `localStorage` under the key `ateam-plan-checklist-v1` (`loadChecked`/`saveChecked` in `app.js`). There is no server or database.
- **Status pills**: `statusClass()` in `app.js` maps table cell text (e.g. "Live", "Build", "Fix — ...") to CSS classes for colored status pills, applied only to the last column of tables whose header is literally "Status" (in `renderTable`).
