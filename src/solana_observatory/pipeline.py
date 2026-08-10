"""Write every required report from the same verified snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .anomalies import build_anomalies, build_threshold_anomalies
from .briefing import build_grounded_briefing
from .comparisons import build_comparisons
from .contracts import validate_snapshot
from .renderers import render_html, render_json, render_markdown
from .timeline import load_timeline, validate_timeline


def write_reports(
    snapshot: dict[str, Any], output_dir: Path
) -> list[Path]:
    snapshot["comparisons"] = build_comparisons(snapshot["metrics"])
    snapshot["anomalies"] = {
        **build_anomalies(snapshot["comparisons"]),
        **build_threshold_anomalies(snapshot["metrics"]),
    }
    if "timeline" not in snapshot:
        timeline_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "history"
            / "solana_timeline.json"
        )
        snapshot["timeline"] = load_timeline(timeline_path)
    else:
        snapshot["timeline"] = validate_timeline(snapshot["timeline"])
    existing_analysis = snapshot.get("analysis")
    if (
        not isinstance(existing_analysis, dict)
        or existing_analysis.get("status") != "ok"
        or existing_analysis.get("kind") == "deterministic"
    ):
        snapshot["analysis"] = build_grounded_briefing(snapshot)
    validate_snapshot(snapshot)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        output_dir / "report.json": render_json(snapshot),
        output_dir / "report.md": render_markdown(snapshot),
        output_dir / "index.html": render_html(snapshot),
    }
    for path, contents in outputs.items():
        path.write_text(contents, encoding="utf-8")
    return list(outputs)
