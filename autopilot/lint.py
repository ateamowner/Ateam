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

# Broad emoji ranges.
_EMOJI_CHAR = (
    "[\U0001F300-\U0001FAFF"   # pictographs, symbols, supplemental
    "\U0001F1E6-\U0001F1FF"    # regional indicators
    "☀-➿"            # misc symbols and dingbats
    "]"
)
# A whole grapheme cluster counts as one emoji. Ant's facepalm is
# U+1F926 + ZWJ + U+2642 + VS16, which is one emoji to a reader and would
# otherwise be counted as two and trip the ceiling on its own.
_EMOJI = re.compile(
    rf"{_EMOJI_CHAR}️?(?:‍{_EMOJI_CHAR}️?)*"
)

_HASHTAG = re.compile(r"(?<!\w)#\w+")
# 10-digit US numbers in any common shape: 9379392936, 937-939-2936, (937) 939-2936
_PHONE = re.compile(r"(?<!\d)(?:\(\d{3}\)\s*|\d{3}[-.\s])\d{3}[-.\s]?\d{4}(?!\d)")
_EM_DASH = re.compile(r"[—–]")
# Narrating the picture. Ant's note on example 2: he does not want the obvious
# stated. The image already carries BEFORE and AFTER labels, so telling the
# reader which side is which spends a line and gives nothing back.
_IMAGE_NARRATION = re.compile(
    r"\b(before on the (left|top)|after on the (right|bottom)|"
    r"on the left|on the right|swipe (to see|right|through)|as you can see|"
    r"in (the|this) (photo|picture|image)|pictured (above|below)|"
    r"check out (this|these) (photo|pic|picture))\b",
    re.IGNORECASE,
)
# Only consecutive exclamation points. Ant genuinely writes "?!?" and that is
# his voice, not a violation, so the pattern deliberately does not match it.
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

    if _IMAGE_NARRATION.search(text):
        problems.append(
            Violation(
                "narrates-the-image",
                "the photo already says this, use the line for what it cannot show",
            )
        )

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


# --- specificity -----------------------------------------------------------
#
# Ant picked examples 1, 3, 8 and 10 as sounding most like him. What those four
# share is that each reports a specific real job: a place, a day, and a detail
# you could only have if you were standing there. The six he passed over
# described a category of homeowner instead of a homeowner.
#
# This is advisory rather than blocking. It is the generator's own quality bar,
# used to reject and rewrite its drafts before Ant ever sees them, because a
# post can satisfy every hard rule and still be the wrong post.

_DAY = re.compile(
    r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"this morning|last week|yesterday|today|last month)\b",
    re.IGNORECASE,
)
_NUMBER = re.compile(
    r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty|"
    r"thirty|ninety|once|twice|first|second)\b",
    re.IGNORECASE,
)
# Double quotes only. An apostrophe is not a quotation, and including one made
# every contraction look like reported speech.
_QUOTE = re.compile(r"[\"“][^\"“”]{6,}[\"”]")
_PERSON = re.compile(
    r"\b(homeowner|neighbou?r|customer|she|he|they|kid|my son|my daughter|guy|lady)\b",
    re.IGNORECASE,
)
# The second kind of concrete. Example 10 reports no job at all and Ant still
# picked it, because it spells out exactly how the thing works: we pick your
# months, same crew, you don't have to call. Mechanics are as concrete as a
# place name, and a scorer that only counted job anchors called that post thin.
_MECHANICS = re.compile(
    r"\b(we pick|we just show up|same crew|same time of year|one trip|one setup|"
    r"one price|one crew|one day|starts after|you don't have to|"
    r"tell us to|no games|inside and out|costs less than)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Specificity:
    score: int
    anchors: list[str]
    missing: list[str]

    @property
    def grounded(self) -> bool:
        """Two anchors is the floor. Every approved example clears it."""
        return self.score >= 2


def specificity(text: str, settings: Settings) -> Specificity:
    """How concretely a draft is grounded.

    Two ways to be concrete, and a post needs two anchors from either family:
    report a real job, or spell out exactly how the thing works.
    """
    anchors, missing = [], []

    def note(hit: bool, name: str) -> None:
        (anchors if hit else missing).append(name)

    note(any(n.lower() in text.lower() for n in settings.neighborhoods), "place")
    note(bool(_DAY.search(text)), "when")
    note(bool(_NUMBER.search(text)), "number")
    note(bool(_PERSON.search(text)), "person")
    note(bool(_QUOTE.search(text)), "quote")

    # Mechanics count individually rather than as one yes/no. Example 10 is
    # built from four separate ones and nothing else, and collapsing them to a
    # single anchor scored Ant's own approved post as the thinnest in the file.
    mechanics = {m.group(0).lower() for m in _MECHANICS.finditer(text)}
    if mechanics:
        anchors.extend(f"mechanics:{m}" for m in sorted(mechanics)[:3])
    else:
        missing.append("mechanics")

    return Specificity(len(anchors), anchors, missing)


def carries_price(text: str) -> bool:
    """True if the copy quotes a figure, which forces explicit approval.

    Offer posts always need Ant's yes. This makes the reason auditable rather
    than implicit in the scheduler.
    """
    return bool(_PRICE.search(text))
