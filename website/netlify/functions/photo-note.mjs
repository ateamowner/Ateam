/*
 * "What we noticed" — server-side photo look at step 4 of /estimate/.
 *
 * WHY THIS IS A FUNCTION AND NOT A fetch() IN THE PAGE
 * ----------------------------------------------------
 * The original estimator called api.anthropic.com straight from the browser
 * with no API key attached, so it never once worked in production — it fell
 * into its catch block every time and showed a fallback line claiming Anthony
 * had already looked at the photo, which he had not.
 *
 * The fix is not "add the key to the page." Page source is public: a key in
 * client-side JS is a key anyone can read and spend. It lives here, in
 * process.env, where only Netlify's build/runtime can see it.
 *
 * DEGRADATION IS THE WHOLE DESIGN
 * -------------------------------
 * This is a nice-to-have on a lead form. It must never cost a lead, delay a
 * submission, or show an error to a customer. Every failure path — no API key
 * configured, oversized image, model refusal, timeout, upstream 500 — returns
 * HTTP 200 with { unavailable: true }, and the estimator simply doesn't draw
 * the card. Nothing here is on the critical path to a submitted form; the
 * photo itself rides along on the Netlify Forms POST regardless.
 *
 * SETUP
 * -----
 * Netlify dashboard -> Site configuration -> Environment variables ->
 * ANTHROPIC_API_KEY. Until that is set the card is simply absent, which is
 * the correct behaviour, not a bug.
 */

import Anthropic from "@anthropic-ai/sdk";

// Netlify's synchronous functions are capped at 10s, so this whole thing
// lives inside a hard wall. Measured against the deploy preview with a real
// job photo: 7.0s and 8.5s end to end at 1024px / 300 max_tokens — close
// enough to the ceiling that responses were being thrown away. The page now
// sends 768px and this asks for fewer tokens, which brings a typical call to
// roughly half the budget.
//
// 9s, not 8s: at 8s we were aborting calls that would still have come back
// inside Netlify's window. Better to let the platform draw the line than to
// discard a good answer a fraction early.
const CALL_TIMEOUT_MS = 9000;

// The page downscales to ~768px before sending. This is a backstop against a
// hand-crafted request, not the normal path.
const MAX_BASE64_CHARS = 1_500_000; // ~1.1MB decoded
const ALLOWED_MEDIA = ["image/jpeg", "image/png", "image/webp", "image/gif"];

const SYSTEM_PROMPT = `You are looking at a photo a homeowner just uploaded to A-Team Contracting, an exterior cleaning company in Tipp City, Ohio. They do window cleaning, pressure washing, soft washing, roof cleaning, gutter cleaning and concrete cleaning.

Write 2-3 short sentences, under 50 words total, describing what you can actually see on this property that relates to exterior cleaning: siding condition, roof streaking, driveway or walkway staining, gutter grime, window count or accessibility, landscaping that affects access.

Rules:
- Only describe what is genuinely visible. Never invent detail. If the photo is dark, blurry, or not of a building's exterior, say plainly that you cannot make much out from this one and that the crew will look at it directly.
- Never state or imply a price, a discount, or how long a job will take. The page shows its own pricing.
- Never promise that anyone has personally reviewed the photo, and never claim work will definitely be needed.
- Warm and plain-spoken, like a contractor glancing at a photo on his phone. No sales language, no exclamation marks, no bullet points, no headings. Prose only.`;

const unavailable = () =>
  new Response(JSON.stringify({ unavailable: true }), {
    status: 200,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405, headers: { Allow: "POST" } });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return unavailable();

  let body;
  try {
    body = await req.json();
  } catch {
    return unavailable();
  }

  // Expects a data URL exactly as FileReader / canvas.toDataURL() produces it.
  const match = /^data:([a-z/+.-]+);base64,(.+)$/i.exec(String(body?.image || ""));
  if (!match) return unavailable();

  const mediaType = match[1].toLowerCase();
  const data = match[2];
  if (!ALLOWED_MEDIA.includes(mediaType)) return unavailable();
  if (data.length > MAX_BASE64_CHARS) return unavailable();

  // The quiz answers, so the note can talk about the surfaces they picked
  // rather than everything in the frame. Clamped — this is attacker-reachable
  // input heading into a prompt.
  const services = String(body?.services || "").slice(0, 200);
  const homeSize = String(body?.home_size || "").slice(0, 60);

  const client = new Anthropic({
    apiKey,
    timeout: CALL_TIMEOUT_MS,
    maxRetries: 0, // A retry cannot fit inside the function's 10s budget.
  });

  try {
    // No extended thinking here on purpose. This is a two-sentence observation,
    // not a reasoning task, and the 10s function ceiling is a hard wall — the
    // right trade is a fast answer or no card at all. max_tokens is 200 for
    // the same reason: the note is capped at ~50 words, so anything more is
    // latency we cannot afford.
    const message = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 200,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: "user",
          content: [
            { type: "image", source: { type: "base64", media_type: mediaType, data } },
            {
              type: "text",
              text:
                `Photo of the customer's property.\n` +
                (homeSize ? `They described the home as: ${homeSize}.\n` : "") +
                (services ? `They are asking about: ${services}.\n` : "") +
                `Write the 2-3 sentence note.`,
            },
          ],
        },
      ],
    });

    // Must be checked before touching content — on a refusal there is no text
    // block to read, and indexing content[0] would throw.
    if (message.stop_reason === "refusal") return unavailable();

    const note = message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join(" ")
      .trim();

    if (!note) return unavailable();

    return new Response(JSON.stringify({ note }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
    });
  } catch (err) {
    // Logged for the Netlify function log, never surfaced to the customer.
    console.error("photo-note failed:", err?.message || err);
    return unavailable();
  }
};
