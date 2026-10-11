#!/usr/bin/env python3
"""Validate generated profile cards and switch README images to local SVGs.

Never switch the README while a card is missing or generation has failed.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CARD_DIR = ROOT / "profile-summary-card-output" / "github_dark"

# Match the five cards that are currently embedded in the profile README.
CARDS = (
    ("profile-details", "0-profile-details.svg"),
    ("stats", "3-stats.svg"),
    ("productive-time", "4-productive-time.svg"),
    ("repos-per-language", "1-repos-per-language.svg"),
    ("most-commit-language", "2-most-commit-language.svg"),
)
OLD_HOST = "https://github-profile-summary-cards-y74b.vercel.app/api/cards"
ERROR_MARKERS = (
    "cards are temporarily rate limited",
    "rate limit exceeded",
    "bad credentials",
    "error!!!",
)

def main() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = []

    for endpoint, filename in CARDS:
        path = CARD_DIR / filename
        if not path.is_file() or path.stat().st_size < 200:
            raise SystemExit(f"Missing or suspiciously small generated card: {path}")

        svg = path.read_text(encoding="utf-8")
        if (not re.search(r"<svg\b", svg) or "</svg>" not in svg
                or any(marker in svg.lower() for marker in ERROR_MARKERS)):
            raise SystemExit(f"Generated card does not look valid: {path}")

        old = f"{OLD_HOST}/{endpoint}?username=SwiftExplorer567&theme=github_dark"
        if endpoint == "productive-time":
            old += "&utcOffset=3"
        new = f"./profile-summary-card-output/github_dark/{filename}"
        if old not in text and new not in text:
            raise SystemExit(f"Cannot find existing README reference for {endpoint}")
        replacements.append((old, new))

    # Only write after ALL five cards have passed validation.
    for old, new in replacements:
        text = text.replace(old, new)
    if text != README.read_text(encoding="utf-8"):
        README.write_text(text, encoding="utf-8")
        print("README now serves locally generated profile cards.")
    else:
        print("README already references locally generated cards.")

if __name__ == "__main__":
    main()
