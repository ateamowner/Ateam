# A-Team Contracting — 90-Day Plan Dashboard

A static, no-backend dashboard for the A-Team Contracting 90-Day Business &
Systems Plan: mission, offer ladder, current state, workflow/automation
tables, the 90-day timeline, KPI targets, risks, and a "Do This Week"
checklist.

## Structure

- `index.html` — page layout/sections (internal 90-day plan dashboard).
- `plan-data.js` — all plan content as a single `PLAN` object. Edit this file
  to update the plan; the page re-renders from it automatically.
- `app.js` — renders `plan-data.js` into `index.html`, computes the active
  90-day phase from today's date, and persists checklist state in the
  browser's `localStorage` (no server, no database).
- `quote.html` — public lead-capture landing page ("Get a Free Quote"),
  linked from the dashboard hero. Submits via Netlify Forms (no backend
  required) and redirects to `thank-you.html` on success.
- `thank-you.html` — confirmation page shown after a quote request submits.
- `styles.css` — brand system (Orange `#F58220`, Blue `#1B5B98`, Charcoal
  `#333333`; Anton headlines / Montserrat body / Caveat accent), plus the
  `.lp-*` classes used by the landing/thank-you pages.
- `netlify.toml` — publishes the repo root as-is, no build step.

## Lead form (quote.html)

The quote request form uses [Netlify Forms](https://docs.netlify.com/forms/setup/):
it's a plain HTML `<form>` with `data-netlify="true"` and a `bot-field`
honeypot for spam — no server code needed. Once deployed to Netlify,
submissions show up under Site settings → Forms, and Netlify can be
configured there to email/notify on new leads. Field values map directly to
column names (`name`, `phone`, `email`, `address`, `service`, `hear_about`,
`message`) for easy export or Zapier/automation hookup.

## Text notifications via Zapier

New leads text the owner's cell at (937) 270-2452. Netlify Forms remains the
system of record; `lead-form.js` additionally POSTs each submission to a
Zapier Catch Hook, so a webhook failure can never cost a lead.

**One-time setup** (the webhook URL only exists once the Zap is created, so
this step has to happen in the Zapier UI):

1. In Zapier, create a Zap with trigger **Webhooks by Zapier → Catch Hook**.
2. Copy the custom webhook URL Zapier generates.
3. Paste it into `ZAPIER_WEBHOOK_URL` at the top of `lead-form.js`, then
   deploy.
4. Submit a test lead on `/quote.html` so Zapier can capture a sample and
   learn the field names.
5. Add action **SMS by Zapier → Send SMS**. That connection is already
   verified to (937) 270-2452, so there is no "to" field to fill in — it
   only takes the message body.
6. Suggested message (SMS by Zapier truncates at 153 characters, so keep it
   tight):

   ```
   New A-Team lead: {{name}} · {{phone}} · {{service}} · {{address}}
   ```

7. Turn the Zap on.

Fields posted to the hook: `name`, `phone`, `email`, `address`, `service`,
`hear_about`, `message`, plus `submitted_at` and `page`. The honeypot and
Netlify's internal `form-name` field are stripped before sending.

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
