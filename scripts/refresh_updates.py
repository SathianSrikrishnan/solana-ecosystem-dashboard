"""Refresh official Solana news and named upgrade signals."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.official_updates import parse_official_updates
from solana_observatory.pipeline import write_reports

RSS_URL = "https://solana.com/news/rss.xml"
ALPENGLOW_URL = "https://solana.com/upgrades/alpenglow"
SIMD_RAW_URL = "https://raw.githubusercontent.com/solana-foundation/solana-improvement-documents/main/proposals/0525-reduce-slot-times.md"


def _fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Solana-Observatory/0.3 (+public-bounty-dashboard)"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        metrics = parse_official_updates(
            _fetch(RSS_URL), _fetch(ALPENGLOW_URL), _fetch(SIMD_RAW_URL),
            collected_at=collected_at,
        )
        snapshot["metrics"].update(metrics)
        snapshot["generated_at"] = collected_at
        written = write_reports(snapshot, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Official updates refresh failed: {error}", file=sys.stderr)
        return 1
    for path in written: print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
