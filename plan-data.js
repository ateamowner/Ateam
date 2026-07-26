// A-Team Contracting — 90-Day Business & Systems Plan
// Structured content pulled from the source plan. Edit this file to update
// the dashboard; index.html/app.js just render whatever is here.

const PLAN = {
  meta: {
    company: "A-Team Contracting",
    subtitle: "90-Day Business & Systems Plan",
    tagline: "Workflow Optimization · Automation · Growth Timeline",
    preparedFor: "Anthony Leonard, Owner",
    location: "Tipp City, Ohio · Serving Greater Dayton",
    contact: "(937) 939-2936 · Owner@ateamcontractings.com · ateamcontractings.com",
    quote: "“Jobs are done best when you work with A-Team!”",
    // Day 1 of the 90-day clock. Change this if the plan's start date shifts.
    startDate: "2026-07-26",
  },

  mission: [
    "10+ new leads/followers every week — consistent, not spurts",
    "Lead gen, social posting, referral follow-up, and phone replies run on automation, not on Ant",
    "2 uninterrupted hours a day with the family — phone down, work off",
  ],

  offerLadder: [
    {
      rung: "Rung 1 — Window Cleaning (the hook)",
      desc: "The easy yes. Low price, fast job, recurring by nature. This is what leads with in every ad, every post, every first DM. It gets A-Team on the property — that's the whole job of Rung 1.",
    },
    {
      rung: "Rung 2 — Windows + Wash Bundle (the upsell)",
      desc: "Sold at the estimate, not after. “While we're here” pricing on driveway/walkway pressure washing or siding/roof softwashing added to the window job. This is where ticket size jumps.",
    },
    {
      rung: "Rung 3 — Clean Club (the lock-in)",
      desc: "Recurring windows + exterior wash on a repeating schedule. $300 non-refundable deposit + $75/month, auto-pay via Stripe. Evergreen membership framing, not a fixed-term contract pitch.",
    },
  ],

  currentState: {
    working: [
      "Clean Club has real, paying accounts — including a $1,299.78/month commercial client (Evans Motors) and an accepted deal at Key Chrysler.",
      "BBB Accreditation achieved at an A+ rating.",
      "AIRA AI receptionist is live on the business line, answering calls automatically.",
      "AutoGTM cold outreach (“Madison” persona) is generating warm commercial leads; Ant steps in once a lead responds.",
      "Brand system (colors, fonts, logo, voice, pricing format) is locked and consistent across documents.",
    ],
    broken: [
      "Website SEO: sitemap.xml and robots.txt are built but not deployed to Netlify. Zero pages indexed. Domain Rating 0. No backlinks.",
      "Local pack visibility: Local Falcon shows average rank positions 10–16 with near-zero share of local voice on core keywords.",
      "AI platform visibility: zero presence on ChatGPT and similar assistants — no citations, no schema.",
      "Zap 5 (review request automation) may be watching the wrong column in the Lead Tracker — flagged as needing a fix.",
      "Zap 3 (one-hour follow-up reminder) and the rest of the automation stack are incomplete.",
      "GBP posting cadence has lapsed and needs to become a standing habit, not a when-I-remember task.",
      "Sister GBP profile (“A-Team Window Cleaning & Pressure Washing”) needs a distinct forwarding number and its own subdomain or domain to avoid a duplicate-listing flag from Google.",
    ],
    inProgress: [
      "Pressure washing rig build — Siamese flow-combining setup on hold pending pump spec confirmation (Honda GX390 13hp vs. Kohler 2.7hp mismatch).",
      "Vehicle wrap design for the 2011 Dodge Ram — mockups complete, not yet printed/installed.",
      "Window cleaning before/after photo library — still needed before content can shift off “wash-first, windows teased.”",
    ],
  },

  workflowTable: {
    headers: ["Function", "Today (manual)", "Target (systemized)"],
    rows: [
      ["Inbound calls", "Ant answers or misses calls between jobs", "AIRA answers every call 24/7, logs the lead, texts Ant a summary"],
      ["Lead capture", "Ant remembers to write it down", "Every call, form, and DM auto-lands in the Lead Tracker with source tagged"],
      ["First response", "Whenever Ant gets to his phone", "Auto-text/email within 5 minutes of a new lead row appearing"],
      ["Estimate follow-up", "Ant tries to remember who hasn't replied", "Day 1 / Day 3 / Day 7 nudge sequence runs automatically"],
      ["Social posting", "Written and posted live, in the moment", "Batched weekly, scheduled to publish without Ant touching a phone"],
      ["Review requests", "Asked in person if Ant remembers", "Auto-triggered the moment a job is marked Completed"],
      ["Referral asks", "Rare, inconsistent", "Auto-triggered 14 days after job completion"],
      ["Estimates/invoices", "Built one at a time, evenings", "Templated ReportLab build — same format every time, 5-minute turnaround"],
      ["Clean Club billing", "N/A — new program", "Stripe auto-pay, zero manual invoicing per member"],
    ],
  },

  automationTable: {
    headers: ["Automation / Zap", "Trigger", "Action", "Status"],
    rows: [
      ["AI phone receptionist", "Inbound call to (937) 939-2936", "AIRA answers, qualifies, logs to Lead Tracker", "Live"],
      ["Lead Tracker as system of record", "New lead from any source", "Row created in Google Sheet with source, contact, service requested", "Live"],
      ["Website/DM capture", "Form submit or social DM", "Auto-routed into Lead Tracker with source tag", "Build"],
      ["Zap 1 — Instant reply", "New row in Lead Tracker", "Auto-text/email within 5 minutes", "Confirm live"],
      ["Zap 2 — Estimate nurture", "Estimate sent, no response", "Day 1 / Day 3 / Day 7 automatic nudge sequence", "Build"],
      ["Zap 3 — One-hour reminder", "Estimate requested", "Internal reminder to Ant if no estimate sent within 1 hour", "Finish build"],
      ["Zap 5 — Review request", "Column G = “Completed” in Lead Tracker", "Auto-send Google review link (bit.ly/4fRa2B5)", "Fix — wrong column"],
      ["Referral ask", "14 days after job Completed", "Auto-text asking for a referral, with a small thank-you offer", "Build"],
    ],
  },

  timeline: [
    {
      phase: "Days 1–14 — Foundation",
      startDay: 1,
      endDay: 14,
      items: [
        "Deploy sitemap.xml and robots.txt to Netlify — closes the biggest SEO gap in one afternoon.",
        "Fix Zap 5 to watch Column G (“Completed”), not Column J — review requests start firing correctly.",
        "Finish and activate Zap 3 (one-hour follow-up reminder).",
        "Build Zap 1 confirmation test — send a dummy lead through and verify the 5-minute auto-reply fires.",
        "Place BBB A+ seal on the site (estimate CTA, footer, homepage hero).",
        "Block a recurring calendar slot for GBP posting — twice a week, non-negotiable.",
      ],
    },
    {
      phase: "Days 15–30 — Fill the Follow-Up Gaps",
      startDay: 15,
      endDay: 30,
      items: [
        "Build Zap 2 (Day 1/3/7 estimate nurture sequence).",
        "Build the 14-day referral-ask automation.",
        "Shoot and edit the first real batch of window cleaning before/after photos.",
        "Resolve the pressure washer pump spec question — decide matched second unit vs. switching manifold, order parts.",
        "Draft and approve LocalBusiness schema markup for the website.",
      ],
    },
    {
      phase: "Days 31–60 — Scale the Content Engine",
      startDay: 31,
      endDay: 60,
      items: [
        "Shift content mix from “wash-first, windows teased” toward windows-forward now that photos exist.",
        "Launch first citation-building push (directories, schema, structured data) for AI-assistant visibility.",
        "Finalize sister GBP profile: secure distinct forwarding number, stand up subdomain, publish listing.",
        "Print and install the vehicle wrap on the 2011 Dodge Ram.",
        "Run first full Weekly Anchor content batch entirely on the new system — no live daily posting.",
      ],
    },
    {
      phase: "Days 61–90 — Prove It and Push Recurring Revenue",
      startDay: 61,
      endDay: 90,
      items: [
        "Audit Local Falcon rankings against Day 1 baseline — target measurable movement out of the 10–16 range.",
        "Review Clean Club roster — push every eligible completed job toward a Rung 3 pitch at the next touchpoint.",
        "Evaluate commercial subcontracting opportunity (Phoenix market) if bandwidth allows — do not let it compete with local systemization.",
        "Full 90-day KPI review against the goals below — decide what becomes the next 90-day cycle's #1 priority.",
      ],
    },
  ],

  kpiTable: {
    headers: ["Metric", "Today", "Day 45", "Day 90"],
    rows: [
      ["New leads / week", "Inconsistent", "6–8", "10+"],
      ["Clean Club members (residential)", "1 active", "3–4", "6+"],
      ["Clean Club members (commercial)", "2 active/committed", "3", "4+"],
      ["Pages indexed on Google", "0", "10+", "All core pages"],
      ["Local Falcon avg. rank", "10–16", "8–12", "Top 10"],
      ["GBP posts / week", "Lapsed", "2", "2 (steady)"],
      ["5-star reviews added", "Baseline", "+8", "+20"],
      ["Family time protected / day", "Inconsistent", "2 hrs, most days", "2 hrs, every day"],
    ],
  },

  risks: [
    "Pump mismatch on the Siamese rig (Honda GX390 13hp vs. Kohler 2.7hp) can stall the pressure washing build if left unresolved — get the spec numbers and decide by Day 14.",
    "Sister GBP profile is a real risk if launched without a distinct phone number and its own subdomain — Google can flag it as a duplicate listing and suppress both.",
    "Zap 5 watching the wrong column means review requests may not be firing at all right now — this is a silent leak in the review pipeline until fixed.",
    "Painting stays deprioritized for local SEO — dead-last rankings, high competition, not where the next 90 days should go.",
    "Shared lead platforms (Angi, etc.) stay off the table — the whole model is owned channels and recurring relationships, not rented leads.",
    "Out-of-state subcontracting (Phoenix) is worth scoping but should never compete with local systemization for Ant's time in this 90-day window.",
  ],

  doThisWeek: [
    "Deploy sitemap.xml + robots.txt to Netlify — 15 minutes, biggest SEO unlock available",
    "Fix Zap 5's trigger column (G, not J) so review requests actually fire",
    "Block two recurring calendar slots for GBP posts and treat them like a job",
    "Get pump model numbers/drive type from both rigs so the Siamese build can move",
    "Pick one day this week to shoot window cleaning before/after photos on a real job",
  ],
};
