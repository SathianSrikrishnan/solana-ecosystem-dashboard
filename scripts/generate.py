"""Generate a live Solana network snapshot and all report formats."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.pipeline import write_reports
from solana_observatory.rpc import SolanaRpcClient, collect_network_results
from solana_observatory.snapshot import (
    build_network_snapshot,
    merge_network_snapshot,
)


def main() -> int:
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rpc_results = collect_network_results(SolanaRpcClient())
    snapshot = build_network_snapshot(rpc_results, collected_at)
    prior_path = ROOT / "output" / "report.json"
    if prior_path.exists():
        prior_snapshot = json.loads(prior_path.read_text(encoding="utf-8"))
        snapshot = merge_network_snapshot(prior_snapshot, snapshot)
    written = write_reports(snapshot, ROOT / "output")
    for path in written:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

