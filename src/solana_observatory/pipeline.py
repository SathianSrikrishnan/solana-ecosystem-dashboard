"""Write every required report from the same verified snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .comparisons import build_comparisons
from .contracts import validate_snapshot
from .renderers import render_html, render_json, render_markdown
from .timeline import load_timeline, validate_timeline


def write_reports(
    snapshot: dict[str, Any], output_dir: Path
) -> list[Path]:
    snapshot["comparisons"] = build_comparisons(snapshot["metrics"])
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
