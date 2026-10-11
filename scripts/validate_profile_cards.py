#!/usr/bin/env python3
"""Fail safely if any generated SVG is missing, invalid, or an API error card."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
CARD_DIR = ROOT / "profile-summary-card-output" / "github_dark"
README = ROOT / "README.md"
ASSET_URL = (
    "https://raw.githubusercontent.com/SwiftExplorer567/SwiftExplorer567/"
    "profile-assets/profile-summary-card-output/github_dark/"
)
FILES = (
    "0-profile-details.svg",
    "1-repos-per-language.svg",
    "2-most-commit-language.svg",
    "3-stats.svg",
    "4-productive-time.svg",
)
ERROR_MARKERS = (
    "cards are temporarily rate limited",
    "rate limit exceeded",
    "bad credentials",
    "error!!!",
    "api rate limit exceeded",
)

def main() -> None:
    readme = README.read_text(encoding="utf-8")
    for filename in FILES:
        path = CARD_DIR / filename
        if not path.is_file() or path.stat().st_size < 300:
            raise SystemExit(f"Missing or suspiciously small profile card: {path}")

        svg = path.read_text(encoding="utf-8")
        if any(marker in svg.lower() for marker in ERROR_MARKERS):
            raise SystemExit(f"Generated an API error card: {path}")
        try:
            root = ET.fromstring(svg)
        except ET.ParseError as exc:
            raise SystemExit(f"Invalid SVG XML in {path}: {exc}") from exc
        if root.tag not in ("svg", "{http://www.w3.org/2000/svg}svg"):
            raise SystemExit(f"Unexpected SVG root tag in {path}: {root.tag}")
        if f'src="{ASSET_URL}{filename}"' not in readme:
            raise SystemExit(f"README does not reference the asset-branch SVG: {filename}")

    print("All five generated cards and README asset links verified.")

if __name__ == "__main__":
    main()
