"""Voice and platform rules, enforced as blocking checks.

Step 4 wraps this in a regenerate loop so a violation never reaches Ant. The
rules themselves live here so that voice.md, brand.md and the generator all
answer to one implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .config import Settings

# Platform names as written in voice.md headings, mapped to config keys.
PLATFORM_ALIASES = {
    "facebook": "facebook",
    "instagram feed": "instagram",
    "instagram story": "instagram",
    "instagram": "instagram",
    "google business profile": "google_business",
    "google business": "google_business",
    "nextdoor": "nextdoor",
}

SERVICE_WORDS = (
    "window", "windows", "softwash", "soft wash", "pressure wash", "power wash",
    "gutter", "gutters", "roof", "driveway", "walkway", "siding", "patio",
    "concrete", "house wash", "wash", "cleaning", "clean",
)

# Broad emoji ranges. Deliberately excludes the variation selector and ZWJ so a
# multi-codepoint emoji counts once, not three times.
_EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF"   # pictographs, symbols, supplemental
    "\U0001F1E6-\U0001F1FF"    # regional indicators
    "☀-➿"            # misc symbols and dingbats
    "]"
)

_HASHTAG = re.compile(r"(?<!\w)#\w+")
# 10-digit US numbers in any common shape: 9379392936, 937-939-2936, (937) 939-2936
_PHONE = re.compile(r"(?<!\d)(?:\(\d{3}\)\s*|\d{3}[-.\s])\d{3}[-.\s]?\d{4}(?!\d)")
_EM_DASH = re.compile(r"[—–]")
_STACKED_BANG = re.compile(r"!{2,}")
# "leverage" as a verb. The noun ("financial leverage") is allowed.
_LEVERAGE_VERB = re.compile(r"\b(?:to\s+)?leverag(?:e|es|ed|ing)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Violation:
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def _word_boundary_hit(haystack: str, phrase: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", haystack, re.IGNORECASE) is not None


def lint(text: str, platform: str, settings: Settings, bucket: str = "") -> list[Violation]:
    """Return every rule this draft breaks. Empty list means it can publish."""
    key = PLATFORM_ALIASES.get(platform.strip().lower(), platform.strip().lower())
    rules = settings.platform_rules(key)
    problems: list[Violation] = []

    for phrase in settings.banned_phrases:
        if _word_boundary_hit(text, phrase):
            problems.append(Violation("banned-phrase", f'"{phrase}"'))

    if _LEVERAGE_VERB.search(text):
        problems.append(Violation("banned-phrase", '"leverage" used as a verb'))

    if _EM_DASH.search(text):
        problems.append(Violation("em-dash", "use a period or a comma in social copy"))

    if _STACKED_BANG.search(text):
        problems.append(Violation("stacked-exclamation", "one is plenty"))

    max_emoji = rules.get("max_emoji", 2)
    emoji_count = len(_EMOJI.findall(text))
    if emoji_count > max_emoji:
        problems.append(Violation("emoji", f"{emoji_count} found, max {max_emoji}"))

    tags = _HASHTAG.findall(text)
    if key == "instagram":
        max_tags = rules.get("max_hashtags", 5)
        if len(tags) > max_tags:
            problems.append(Violation("hashtags", f"{len(tags)} found, max {max_tags}"))
    elif tags:
        problems.append(
            Violation("hashtags", f"{len(tags)} found, hashtags are Instagram only")
        )

    if not rules.get("allow_phone_in_body", True) and _PHONE.search(text):
        problems.append(
            Violation(
                "phone-in-body",
                f"{key} suppresses posts carrying a 10-digit number, graphics only",
            )
        )

    if key == "google_business":
        visible = rules.get("visible_chars", 100)
        head = text[:visible].lower()
        if not any(n.lower() in head for n in settings.neighborhoods):
            problems.append(
                Violation("gbp-hook", f"no city in the first {visible} characters")
            )
        if not any(w in head for w in SERVICE_WORDS):
            problems.append(
                Violation("gbp-hook", f"no service named in the first {visible} characters")
            )
        max_chars = rules.get("max_chars", 1500)
        if len(text) > max_chars:
            problems.append(Violation("length", f"{len(text)} chars, max {max_chars}"))

    if key == "nextdoor" and rules.get("require_neighborhood_mention"):
        if not any(n.lower() in text.lower() for n in settings.neighborhoods):
            problems.append(
                Violation("nextdoor-local", "name the neighborhood the job was in")
            )

    # Clean Club language guards, wherever the club is mentioned.
    if "clean club" in text.lower():
        if _word_boundary_hit(text, "contract"):
            problems.append(Violation("clean-club", 'never call it a "contract"'))

    if bucket.lower() == "offer":
        problems.extend(_lint_offer(text))

    return problems


# Scarcity claims that need a real date attached.
_SCARCITY = re.compile(
    r"\b(limited time|act fast|hurry|while supplies last|ending soon|last chance)\b",
    re.IGNORECASE,
)
_DATE_HINT = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}\b"
    r"|\b\d{1,2}/\d{1,2}\b"
    r"|\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    re.IGNORECASE,
)
_PRICE = re.compile(r"\$\s?\d")


def _lint_offer(text: str) -> list[Violation]:
    """Offer-specific compliance, added after the Aug 6 review of IMG_0399.

    The retail-value / A-Team Discount / YOUR PRICE structure is a property of
    the graphic, not the caption, so it is checked in the image pipeline where
    the artwork is available. Here we only catch what is visible in the words.
    """
    problems: list[Violation] = []

    if _SCARCITY.search(text) and not _DATE_HINT.search(text):
        problems.append(
            Violation("undated-scarcity", "a scarcity claim needs a real end date")
        )

    return problems


def carries_price(text: str) -> bool:
    """True if the copy quotes a figure, which forces explicit approval.

    Offer posts always need Ant's yes. This makes the reason auditable rather
    than implicit in the scheduler.
    """
    return bool(_PRICE.search(text))
