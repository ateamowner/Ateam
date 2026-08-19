# Setup — what Ant has to do, and in what order

Everything here is one-time. Once it's done the system runs without him.

Ordered by what unblocks the most. Item 1 alone unblocks the rest of Step 5,
Step 6, and the photo pipeline running against live Drive.

---

## 1. Google service account — the real blocker

**Why:** the system posts at 9:00 AM whether or not anyone is logged in. It
needs its own Google identity. The connectors in a chat session belong to
whoever is chatting; a cron job at dawn has no one to borrow from.

**One correction to something I said earlier:** I cannot generate the service
account address. It has to be created inside Google Cloud Console under Ant's
account, and then he sends me the address. I had it backwards.

### The steps

1. Go to **console.cloud.google.com** and sign in as `owner@ateamcontractings.com`.
2. Top bar, project dropdown → **New Project**. Name it `ateam-autopilot`.
   No billing needed. The APIs below are free at our volume.
3. Search bar → **Google Drive API** → **Enable**.
4. Search bar → **Google Sheets API** → **Enable**.
5. Left menu → **IAM & Admin** → **Service Accounts** → **Create service account**.
   - Name: `autopilot`
   - Skip the optional role and access steps. It needs no project roles at all;
     access comes from the file shares in step 7.
6. Click the new account → **Keys** tab → **Add key** → **Create new key** →
   **JSON**. A file downloads. **That file is the password to everything it can
   reach.** Do not email it or put it in Drive.
7. Copy the service account email. It looks like
   `autopilot@ateam-autopilot.iam.gserviceaccount.com`.

### Then three shares, two minutes

Open each of these and use the normal **Share** button, exactly as you would
share with a person. Paste the service account email.

| What | Access | Why |
|---|---|---|
| **Job Photos** folder | Editor | Reads new photos, moves used ones to `Posted/` |
| **Social Media Calendar** sheet | Editor | Writes the `Queue` tab |
| **Lead Tracker** sheet | Viewer | Reads leads for the Friday report |

Untick "Notify people" — nobody is there to read the email.

### Getting the key to the system

Same place the Anthropic key went:

**github.com/ateamowner/Ateam** → Settings → Secrets and variables → Actions →
**New repository secret**

- Name: `GOOGLE_SERVICE_ACCOUNT_JSON`
- Value: the entire contents of the downloaded JSON file, pasted whole

Then delete the downloaded file from the laptop. GitHub has it now.

### If Google Cloud Console is too much

There is a lower-ceiling alternative: the Zapier account already has Google
Sheets connected, so the calendar writes could go through a Zapier webhook with
no Google Cloud involvement at all.

It does not solve the photo pipeline. Reading a folder and pulling image bytes
through Zapier into a scheduled job is awkward and fragile, and the photo
pipeline is the part that produces proof posts. Recommend doing the service
account properly once rather than working around it twice.

---

## 2. Meta — Instagram feed and stories

Decided Aug 6: stories are in scope for v1, which means a Meta app. That same
app also carries Instagram feed posts, so the Zapier Instagram connection is
not needed.

1. **business.facebook.com** → confirm the A-Team Facebook Page and the
   Instagram account are both in the same Business portfolio, and that the
   Instagram account is a **Professional** account linked to the Page. Publishing
   fails without both.
2. **developers.facebook.com** → My Apps → **Create App** → type **Business**.
3. In the app, add the **Instagram** product and request
   `instagram_business_content_publish`.
4. Collect three values and send them over:
   - Facebook **Page ID**
   - Instagram **Business Account ID**
   - A **long-lived access token**

Secrets: `META_PAGE_ID`, `META_IG_BUSINESS_ID`, `META_ACCESS_TOKEN`.

About twenty minutes, once. Long-lived tokens expire after roughly 60 days, so
the system will warn before that happens rather than failing silently on a
Tuesday morning.

---

## 3. Zapier — three webhooks

Facebook Pages and Google Business Profile are already connected on the Zapier
account, which is why neither needs a developer app. What is missing is a way
for a scheduled job to trigger them.

For each of the three below: **Create Zap** → trigger **Webhooks by Zapier** →
**Catch Hook** → copy the URL → add the action → publish.

| Zap | Action to add | Secret name |
|---|---|---|
| Post to Facebook | Facebook Pages → Create Page Photo | `ZAPIER_HOOK_FACEBOOK` |
| Post to Google Business | Google Business Profile → Create Post | `ZAPIER_HOOK_GBP` |
| Text Ant | SMS by Zapier → Send SMS | `ZAPIER_HOOK_SMS` |

Send the three webhook URLs and they go in as secrets. About ten minutes.

---

## 4. Netlify — the approval page

Needed for Step 6, not before. The approval page and its handler deploy to the
existing Netlify site alongside the 90-Day Plan dashboard, so there is nothing
new to create. Flagged here only so it is not a surprise later.

Secret: `APPROVAL_BASE_URL`, which is just the site URL.

---

## Where things stand

Done:

- `ANTHROPIC_API_KEY` — loaded, and verified working by a live caption run

Outstanding, in order of what they unblock:

1. `GOOGLE_SERVICE_ACCOUNT_JSON` — blocks calendar writes, live photo pipeline, Step 6
2. `META_PAGE_ID`, `META_IG_BUSINESS_ID`, `META_ACCESS_TOKEN` — block Instagram
3. `ZAPIER_HOOK_FACEBOOK`, `ZAPIER_HOOK_GBP`, `ZAPIER_HOOK_SMS` — block publishing and texts
4. `APPROVAL_BASE_URL` — blocks the approval page

`python -m autopilot.check` prints which of these are still missing on every run.

---

## What is deliberately not on this list

Things the original brief expected Ant to do that turned out to be unnecessary:

- Applying to Google for Business Profile API posting access. Zapier already
  holds it.
- Creating a Meta developer app in order to post to Facebook. Zapier covers
  Facebook. The Meta app is only for Instagram.
- Finding a way to post to Nextdoor automatically. There isn't one for a
  business this size. Three pastes a week, about ninety seconds total.
