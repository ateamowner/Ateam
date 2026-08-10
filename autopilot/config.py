"""Loads and validates every configuration input the system depends on.

Nothing else in the codebase reads a config file directly. If a value is
missing or malformed, this module raises here rather than letting a bad value
reach a publisher.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).parent / "config"

# Values written as "env:NAME" are resolved from the environment at load time.
_ENV_PREFIX = "env:"


class ConfigError(Exception):
    """Raised when configuration is missing, malformed, or internally inconsistent."""


@dataclass
class Voice:
    """The voice rules plus Ant's approved example posts."""

    raw: str
    examples: list["VoiceExample"] = field(default_factory=list)


@dataclass
class VoiceExample:
    index: int
    bucket: str
    platform: str
    body: str


@dataclass
class Settings:
    data: dict
    voice: Voice
    brand: str
    banned_phrases: list[str]

    # --- convenience accessors, so callers never index raw dicts ---

    @property
    def timezone(self) -> str:
        return self.data["business"]["timezone"]

    @property
    def neighborhoods(self) -> list[str]:
        return self.data["business"]["neighborhoods"]

    @property
    def public_phone(self) -> str:
        return self.data["business"]["public_phone"]

    def platform_rules(self, platform: str) -> dict:
        return self.data.get("platform_rules", {}).get(platform, {})

    def weekly_post_counts(self) -> dict[str, int]:
        """Posts per week per platform, derived from the cadence block.

        Kept here rather than hardcoded so the 34-a-week arithmetic in the
        architecture doc stays in sync with what the scheduler actually does.
        """
        c = self.data["cadence"]
        counts = {
            "facebook": c["facebook"]["posts_per_day"] * 7,
            "instagram_feed": c["instagram_feed"]["posts_per_day"] * 7,
            "instagram_story": c["instagram_story"]["posts_per_day"] * 7,
            "google_business": len(c["google_business"]["days"]),
            "nextdoor": len(c["nextdoor"]["days"]),
        }
        return counts


def _resolve_env(value):
    """Replace "env:NAME" markers with the environment value, or None if unset."""
    if isinstance(value, str) and value.startswith(_ENV_PREFIX):
        return os.environ.get(value[len(_ENV_PREFIX):])
    if isinstance(value, dict):
        return {k: _resolve_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env(v) for v in value]
    return value


# Matches "### 3. Proof · Google Business Profile"
_EXAMPLE_HEADING = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s+·\s+(.+?)\s*$", re.MULTILINE)


def parse_voice_examples(raw: str) -> list[VoiceExample]:
    """Pull the example posts out of voice.md.

    Examples are blockquotes under a numbered heading. Everything that is not a
    blockquote line (the italic annotation under each one) is ignored.
    """
    examples: list[VoiceExample] = []
    matches = list(_EXAMPLE_HEADING.finditer(raw))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        section = raw[start:end]

        lines = []
        for line in section.splitlines():
            stripped = line.strip()
            if stripped.startswith(">"):
                lines.append(stripped.lstrip(">").strip())
        # Blockquote soft-wrapping: join wrapped lines, keep blank lines as breaks.
        body = "\n".join(lines).strip()
        if not body:
            continue
        examples.append(
            VoiceExample(
                index=int(m.group(1)),
                bucket=m.group(2).strip(),
                platform=m.group(3).strip(),
                body=body,
            )
        )
    return examples


def _load_banned(path: Path) -> list[str]:
    phrases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            phrases.append(line.lower())
    return phrases


def _validate(data: dict) -> None:
    mix = data.get("content_mix", {})
    total = sum(mix.values())
    if abs(total - 1.0) > 1e-6:
        raise ConfigError(f"content_mix must sum to 1.0, got {total}")

    nd = data["cadence"]["nextdoor"]
    if len(nd["days"]) > nd["hard_cap_per_week"]:
        raise ConfigError(
            f"nextdoor cadence has {len(nd['days'])} days but a hard cap of "
            f"{nd['hard_cap_per_week']} per week"
        )

    for platform in ("google_business", "nextdoor"):
        rules = data["platform_rules"][platform]
        if rules.get("allow_phone_in_body"):
            raise ConfigError(
                f"{platform} must not allow a phone number in body text. "
                "Google suppresses those posts and Nextdoor reads them as ads."
            )

    assets = data["assets"]
    if assets["logo_web_1200_id"] == assets["logo_master_id_DO_NOT_USE"]:
        raise ConfigError("logo_web_1200_id is pointing at the gray-background master")


def load(config_dir: Path | None = None) -> Settings:
    """Load config.yaml, voice.md, brand.md and banned.txt, and validate them."""
    d = config_dir or CONFIG_DIR
    try:
        data = yaml.safe_load((d / "config.yaml").read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"missing config.yaml in {d}") from exc

    _validate(data)
    data["credentials"] = _resolve_env(data.get("credentials", {}))

    voice_raw = (d / "voice.md").read_text(encoding="utf-8")
    voice = Voice(raw=voice_raw, examples=parse_voice_examples(voice_raw))

    return Settings(
        data=data,
        voice=voice,
        brand=(d / "brand.md").read_text(encoding="utf-8"),
        banned_phrases=_load_banned(d / "banned.txt"),
    )


def missing_credentials(settings: Settings) -> list[str]:
    """Credential keys that are declared but not yet present in the environment."""
    return [k for k, v in settings.data.get("credentials", {}).items() if not v]
