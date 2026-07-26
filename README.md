# A-Team Contracting — 90-Day Plan Dashboard

A static, no-backend dashboard for the A-Team Contracting 90-Day Business &
Systems Plan: mission, offer ladder, current state, workflow/automation
tables, the 90-day timeline, KPI targets, risks, and a "Do This Week"
checklist.

## Structure

- `index.html` — page layout/sections.
- `plan-data.js` — all plan content as a single `PLAN` object. Edit this file
  to update the plan; the page re-renders from it automatically.
- `app.js` — renders `plan-data.js` into `index.html`, computes the active
  90-day phase from today's date, and persists checklist state in the
  browser's `localStorage` (no server, no database).
- `styles.css` — brand system (Orange `#F58220`, Blue `#1B5B98`, Charcoal
  `#333333`; Anton headlines / Montserrat body / Caveat accent).
- `netlify.toml` — publishes the repo root as-is, no build step.

## Updating the plan

Edit the relevant array/object in `plan-data.js` (e.g. `PLAN.timeline`,
`PLAN.kpiTable`, `PLAN.doThisWeek`). No other file needs to change for
content edits. `PLAN.meta.startDate` controls which 90-day phase is shown as
"active."

## Running locally

No build step required — open `index.html` directly in a browser, or serve
the directory with any static file server, e.g.:

```
python3 -m http.server 8000
```

## Deploying

Point Netlify at this repo; `netlify.toml` publishes the root directory with
no build command.
