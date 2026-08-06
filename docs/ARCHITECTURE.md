# A-Team Social Autopilot — Architecture Preview

**Status:** Step 1 of 9. No code written yet. Waiting on Ant's approval.
**Date:** August 6, 2026

---

## 0. What I checked before writing this

I did not take the brief's assumptions on faith. I inspected the live accounts:
the Zapier connections, the Google Drive folders, the Social Calendar Sheet, and
current platform API availability. Five things came back different from what the
brief assumed. Three of them make the build easier. Two make it harder.

**Good news**

1. **Google Business Profile posting is already automatable.** The brief assumed
   we'd hit Google's restricted-API wall and fall back to copy-paste. We don't
   have to. The Zapier account has **Google Business Profile connected with a
   working `Create Post` action**. Zapier holds the approved API access, so we
   inherit it. GBP is fully automated. Ant touches nothing.
2. **Facebook needs no Meta developer app.** Zapier has **Facebook Pages
   connected** with Create Page Post, Create Page Photo, Create Page Video, and
   Page Post Insights. That covers publishing *and* metrics. No app review, no
   token expiry babysitting.
3. **The Job Photos folder ID was blank in the brief. I found it.**
   `17fWnFBBh778RsyR20SUcO0y-GPlNaYlN`. The photos are not in it directly —
   they're one level down in a **"Before and after"** subfolder. The watcher has
   to recurse, or it would have watched an empty folder forever and silently
   never posted a proof photo.

**Bad news**

4. **The SMS reply loop does not work with what's connected.** The Twilio
   connector in this workspace is Twilio's *documentation* server — it can look
   up API docs, it cannot send or receive a message on an account. What we do
   have is **SMS by Zapier**, which is **send-only and text-only**. It cannot
   receive Ant's `1` / `2` / `5` replies, and it cannot attach the image.
   The reply-with-a-digit loop as specified needs a real Twilio account. See §7 —
   there is a good workaround that ships today.
5. **Nextdoor has no posting API for us.** The Zapier Nextdoor app is read-only
   (ad conversion tracking). Nextdoor's Publish API exists but is gated to
   approved partner categories, and a solo exterior-cleaning company won't clear
   it. Nextdoor stays one-tap manual. That is the honest answer, and at 3/week
   it costs Ant about 90 seconds a week.

**And one thing about the photos themselves that would have broken the pipeline
on day one:** a large share of the files in the Before-and-after folder are
**HEIF images from an iPhone with `.png` filenames**. Others are JPEGs named
`.PNG`. Several have no extension at all. Pillow will refuse to open the HEIFs
and the run would crash mid-batch. The pipeline sniffs magic bytes, ignores
extensions entirely, and carries `pillow-heif`. There are also **11 near-identical
copies of "Copy of Tuesday Transformation.png"** sitting in the folder — which
is exactly the case perceptual-hash dedup exists for.

---

## 1. The honest cadence math

The brief says "19 posts (14 FB/IG + 3 GBP + 3 Nextdoor)." The stated cadence
actually produces more than that:

| Platform | Per week | Notes |
|---|---:|---|
| Facebook (9:00 AM, 5:30 PM) | 14 | |
| Instagram feed (12:00 PM) | 7 | |
| Instagram story (7:00 PM) | 7 | derived from that day's feed post, not written fresh |
| Google Business Profile (M/W/F 10:00 AM) | 3 | |
| Nextdoor (T/Th/Sat 6:00 PM) | 3 | hard cap, enforced in code |
| **Total pieces** | **34** | of which **27 are original posts**, 7 are derived stories |

The content mix runs against the 27 originals:

| Bucket | Share | Posts/week |
|---|---:|---:|
| Proof (before/after) | 40% | 11 |
| Education | 20% | 5 |
| Offer | 20% | 5 |
| Local / community | 10% | 3 |
| Family / behind-the-scenes | 10% | 3 |

**The photo supply problem this creates.** 11 proof posts a week against a
90-day no-reuse rule is 140+ unique photo assets per quarter. The Drive folder
has roughly 60 images today, and about a third are duplicates or already-composed
graphics. That math does not close.

The fix is to define the no-reuse rule **per platform, not globally**. One job's
before/after can serve Facebook, Instagram, and GBP in the same week with three
different captions — that's normal practice and nobody notices, because almost
nobody follows a local contractor on all three. Under that rule, 11 proof slots
need **5–7 fresh job shoots per week**, which is realistic for Ant's job volume.

**What this means for Ant:** the system needs roughly **6 new job before/afters
per week** to run at full proof ratio. Below 3 unused pairs, it automatically
shifts to the evergreen bank and texts him a nudge, so the calendar never goes
dark — but the proof ratio is what actually generates leads, so this is the one
input the system genuinely needs from him.

---

## 2. Automation truth table — what still touches Ant's hands

| Platform | Status | How | Ant's involvement |
|---|---|---|---|
| **Facebook** | ✅ Fully automated | Zapier → Facebook Pages (connected today) | None |
| **Google Business Profile** | ✅ Fully automated | Zapier → GBP Create Post (connected today) | None |
| **Instagram feed** | ✅ Automated after one connect | Zapier → Instagram for Business *(needs enabling)* | One-time OAuth click |
| **Instagram story** | ⚠️ Needs a Meta app | Graph API container with `media_type=STORIES` | One-time Meta setup, or drop stories |
| **Nextdoor** | 🖐 One-tap | Text/queue page with caption pre-copied | ~30 sec × 3/week |
| **SMS approvals** | ⚠️ Depends on §7 decision | Twilio, or link-to-page | See §7 |
| **Metrics: FB/IG** | ✅ Automated | Zapier Page Post Insights | None |
| **Metrics: GBP** | ⚠️ Partial | Zapier GBP raw GET; Local Falcon for ranking | None |
| **Metrics: Nextdoor** | 🖐 Manual | Ant eyeballs it, or we skip | Optional |

Everything marked ✅ requires nothing from Ant, ever, after setup.
Total ongoing manual time: **about 4 minutes a week**, all of it Nextdoor.

---

## 3. Where the system runs

This is the part the brief didn't specify, and it's the decision everything else
hangs off. The connectors in this chat session are *my* tools — they exist while
someone is talking to Claude. A system that posts at 9:00 AM whether or not
anyone is watching needs its own credentials and its own runtime.

```
┌───────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS  — the brains. Runs on cron, holds the secrets.   │
│                                                                    │
│   */15 * * * *   dispatcher   → is anything due right now? (ET)    │
│   0 */1 * * *    drive watch  → new photos? ingest + classify      │
│   Sun 19:00 ET   planner      → build next week's 27 posts         │
│   Fri 16:00 ET   reporter     → pull metrics, text the 3-liner     │
└───────────┬───────────────────────────────────┬───────────────────┘
            │                                   │
            ▼                                   ▼
┌────────────────────────┐         ┌──────────────────────────────┐
│  GOOGLE (service acct) │         │  ZAPIER CATCH HOOKS          │
│  • Job Photos (read)   │         │  • → Facebook Page post      │
│  • Posted/ archive     │         │  • → GBP local post          │
│  • Calendar Sheet (RW) │         │  • → Instagram feed post     │
│  • Lead Tracker (read) │         │  • → SMS to Ant              │
└────────────────────────┘         └──────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────────┐
│  NETLIFY  — the thin edge. Instant response, no cold scheduler.   │
│   /approve            mobile approval page (thumb-sized buttons)  │
│   /.netlify/functions/sms-inbound     Twilio reply webhook        │
│   /.netlify/functions/approve         records a tap → Sheet       │
└───────────────────────────────────────────────────────────────────┘
```

**Why GitHub Actions and not a server:** free, already where the code lives,
secrets management built in, and if it breaks Ant gets an email instead of
silence. **Why a 15-minute dispatcher instead of one cron per post time:**
GitHub cron has no timezone and drifts under load. The dispatcher wakes up,
asks `zoneinfo("America/New_York")` what time it actually is, and fires anything
due. That is DST-proof and drift-proof. A 9:00 AM post lands by 9:15 worst case.

**Netlify note:** the repo currently deploys the 90-Day Plan dashboard from the
root. Netlify functions coexist with that fine — we add a `[functions]` block
and an `/approve` page to the same site. No second site, no migration.

---

## 4. File tree

```
Ateam/
├─ index.html, app.js, plan-data.js, styles.css   ← existing 90-day dashboard, untouched
├─ netlify.toml                                    ← gains a [functions] block
├─ docs/
│  └─ ARCHITECTURE.md                              ← this file
├─ autopilot/
│  ├─ config/
│  │  ├─ config.yaml          cadence, timezones, thresholds, all IDs
│  │  ├─ voice.md             voice rules + 10 Ant-approved example posts
│  │  ├─ brand.md             colors, fonts, logo rules, pricing display
│  │  └─ banned.txt           linter wordlist (circle back, synergy, ...)
│  ├─ src/
│  │  ├─ drive/               watch (recursive), fetch, archive, manifest
│  │  ├─ images/              normalize · quality gate · classify · pair · brand · reel
│  │  ├─ content/             generate · lint · mix enforcement · evergreen bank
│  │  ├─ schedule/            weekly planner · slot calendar · Sheet writer
│  │  ├─ approve/             SMS batching · reply parser · auto-approve timer
│  │  ├─ publish/             facebook · instagram · gbp · nextdoor(manual queue)
│  │  ├─ metrics/             pull · weekly report
│  │  └─ state/               used_photos.json · phash index · decision log
│  ├─ content/evergreen/      education · offer · local · family banks
│  └─ tests/
├─ netlify/functions/         sms-inbound.js · approve.js
└─ .github/workflows/         dispatch.yml · watch.yml · plan.yml · report.yml
```

---

## 5. Photo pipeline — the failure modes it's built around

```
Drive "Before and after" (recursive)
   │
   ├─▶ SNIFF        magic bytes, not extensions. HEIF/HEIC → pillow-heif.
   │                (Half this folder is HEIF wearing a .png name.)
   ├─▶ NORMALIZE    ImageOps.exif_transpose() FIRST, before any crop or resize.
   │                Nothing downstream sees a pre-transpose pixel.
   ├─▶ DEDUPE       perceptual hash vs used_photos.json + vs the batch itself.
   │                (Catches the 11 "Copy of Tuesday Transformation" clones.)
   ├─▶ QUALITY GATE Laplacian variance for blur · exposure histogram ·
   │                face detect → hold for review · plate/house-number OCR → reject
   ├─▶ CLASSIFY     vision tag: service · before|after · subject · score 1–10
   │                SEEDED BY FILENAME — "PW driveway Centerville" and
   │                "Siding SW Tipp City" already carry service + subject + city.
   │                Free ground truth, and it gives us the neighborhood name.
   ├─▶ PAIR         timestamp proximity + visual similarity + same subject tag.
   │                Mismatched orientation → equal HEIGHT, natural widths.
   │                Never crop to force an aspect ratio.
   ├─▶ BRAND        logo bottom-right, 12% width, 85% opacity.
   │                Transparency via edge flood-fill BFS from all four corners —
   │                NOT color-key, which eats the white interior of the shield.
   │                Source: "ATeam Logo Web 1200.png", never the Master file.
   └─▶ ARCHIVE      → /Job Photos/Posted/YYYY-MM/ + manifest row
```

**On the logo:** the brief names `ATeam_Logo_Web_1200.png`. In Drive it's
`ATeam Logo Web 1200.png` (spaces, not underscores), ID
`1Np9lmVCrhkWjz7LvmkcYRqVuujYpooiY`. The 6.8 MB `ATeam Logo Master.png` is the
gray-background file and is explicitly excluded — a copy of it is also loose in
the Drive root as an untitled upload, so the code matches on file ID, not name.

**Output sizes**, matching the convention Ant already uses in that folder:
`ATeam-BeforeAfter-{topic}-1080x1350-facebook-instagram.jpg` and
`-1080x1080-google-business.jpg`, plus `1080x1920` for stories.

---

## 6. The Calendar Sheet needs a second tab

The Social Media Calendar Sheet today is a **human matrix**: rows are platforms
(Nextdoor, Skool, Google, Yelp, Facebook, Instagram), columns are days of the
week, and caption text lives in the cells. It reads well. It is not writable by
a machine with "explicit column labels on every write," because it has no column
labels — column 4 is "Wednesday," which means something different every week.

**Proposal:** leave Ant's matrix alone as the human view. Add a `Queue` tab that
is a proper labeled table, one row per post, and make it the system's source of
truth:

`post_id · week_of · platform · scheduled_at_et · bucket · anchor · caption ·
image_file_id · image_url · cta_type · cta_url · status · approval_code ·
approved_at · published_at · platform_post_id · reach · engagement · notes`

Every write addresses columns by **header name**, resolved at write time. If Ant
reorders or inserts a column, nothing breaks.

Two things I noticed in the existing sheet worth fixing while we're in there:
the **Nextdoor row has content in all 7 day columns** (the cap is 3), and the
emoji are **mojibake** (`ð¸` where a camera emoji should be) from an encoding
mishap on a previous write. The new writer is UTF-8 end to end.

The sheet also carries **Skool** and **Yelp** rows that aren't in the brief's
cadence. Both are easy adds later — Skool especially, since Ant's existing Skool
copy is the best voice reference material in the whole account. Out of scope for
v1 unless he says otherwise.

---

## 7. The approval loop — one real decision to make

The design calls for MMS to Ant with the image, and single-digit replies. That
needs **inbound** SMS. Here are the two honest paths:

**Option A — Real Twilio account.** Ant creates a Twilio account, buys an
MMS-capable number, gives me the SID and auth token. We get exactly the specified
experience: image + caption arrive as an MMS, he replies `1`, done. Netlify
function catches the inbound webhook and writes the decision to the Sheet.
*Cost: ~$1.15/mo for the number, ~$0.02 per MMS. At 2 batches/day that's roughly
$3–4/month.* Setup: about 10 minutes, one credit card.

**Option B — Link-to-tap, works today, zero new credentials.** SMS by Zapier
sends a plain text at 7:00 AM and 6:00 PM: *"4 posts ready — [link]"*. The link
opens the mobile approval page: image, caption, platform, time, and five big
thumb buttons that do exactly what `1`–`5` do. One tap to open, one tap per post,
or one **Approve all** button.

Option B is arguably *better* for the photo posts, because Ant sees the actual
image full-screen instead of a compressed MMS thumbnail, and "approve all" is one
tap instead of composing a reply. Option A is better when he's got one hand free
on a roof.

**My recommendation: build Option B first, because it ships without waiting on
anything, and it is genuinely good.** Add Option A on top in Step 6 if Ant wants
true SMS replies — the reply parser and the tap handler write to the same place,
so adding Twilio later is a small addition, not a rework.

Everything else in §7 of the brief holds either way: two windows only (7:00 AM,
6:00 PM — never 5–7 PM), 3-hour auto-approve fallback, offer/pricing posts always
requiring an explicit yes, and every decision logged so the generator learns
Ant's taste after 30 days.

---

## 8. What I need from Ant

Ordered by what blocks what. Nothing here takes more than a few minutes.

| # | What | Why | Ant's effort |
|---|---|---|---|
| 1 | **Share 3 things with a Google service account** (I'll generate the address) — the Job Photos folder, the Calendar Sheet, the Lead Tracker Sheet | Lets the unattended system read photos and write the queue | 3 share dialogs, ~2 min |
| 2 | **Anthropic API key** | This is the copywriter. Without it there's no generation engine | Paste one key |
| 3 | **Zapier: enable Instagram for Business + connect the IG account** | The only missing publishing path of the four | One OAuth click |
| 4 | **Zapier: create 4 Catch Hook Zaps** and send me the webhook URLs (FB post, GBP post, IG post, send SMS) | How the cron job reaches the already-authorized publishers | ~15 min in Zapier, or I can write the exact steps |
| 5 | **Decision on §7** — Option A (Twilio) or Option B (link-to-tap) | Determines the approval build | One answer |
| 6 | **Decision on IG Stories** — worth a Meta developer app, or skip stories in v1? | Stories are the one thing Zapier can't do | One answer |
| 7 | *(Optional)* Meta Page ID + IG Business ID + long-lived token | Only if #6 is yes | ~20 min in Meta Business Suite |

**What he does NOT need to do**, contrary to the brief: apply for Google Business
Profile API access, create a Meta developer app for Facebook, or find a way to
post to Nextdoor programmatically.

---

## 9. Build sequence from here

Each step ships working before the next one starts.

| Step | What | Gate |
|---|---|---|
| 1 | **This document** | ⬅ **Waiting on Ant** |
| 2 | Scaffold + `voice.md` (with 10 drafted examples for Ant to approve) + `brand.md` + config | Ant approves the 10 voice examples |
| 3 | Photo pipeline end to end, run against the real Drive folder | Ant sees 5 finished branded before/afters |
| 4 | Generation engine + banned-phrase linter with auto-regenerate | Ant reads 10 generated captions |
| 5 | Scheduler + mix enforcement + `Queue` tab writes | A full week appears in the Sheet |
| 6 | Approval loop (§7 option) | Ant approves a post from his phone |
| 7 | Publishers: Facebook → GBP → Instagram → Nextdoor queue | One real post goes live on each |
| 8 | Metrics + Friday report | Ant gets a real Friday text |
| 9 | **Dry run:** one full week generated, nothing published, Ant reviews everything | Green light to go live |

---

## 10. Definition of done

Ant dumps 20 photos in Drive on Sunday. Sunday night he gets one text and
approves the week. Twice a day he taps or texts a digit. Nextdoor takes him 30
seconds, three times a week. Friday he gets three lines telling him what worked.
Under 5 minutes a day, and he never opens a laptop.

That is achievable with what's connected. The only piece that isn't fully
automatic is Nextdoor, and that's Nextdoor's fault, not the system's.

---

*Jobs are done best when you work with A-Team!*
