"""Execute the three bounded adoption queries after explicit human approval."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_client import execute_query


QUERIES = (8213434, 8264418, 8264526)


def main() -> int:
    api_key = os.environ.get("DUNE_API_KEY", "")
    if not api_key:
        print("DUNE_API_KEY is required for approved query execution.", file=sys.stderr)
        return 1
    total = 0.0
    for query_id in QUERIES:
        cost = execute_query(query_id, api_key)
        total += cost
        print(f"Dune query {query_id} completed: {cost:.4f} credits")
    print(f"Approved Dune refresh completed: {total:.4f} credits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
