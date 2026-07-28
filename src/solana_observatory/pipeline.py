"""Write every required report from the same verified snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .renderers import render_html, render_json, render_markdown


def write_reports(
    snapshot: dict[str, Any], output_dir: Path
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        output_dir / "report.json": render_json(snapshot),
        output_dir / "report.md": render_markdown(snapshot),
        output_dir / "index.html": render_html(snapshot),
    }
    for path, contents in outputs.items():
        path.write_text(contents, encoding="utf-8")
    return list(outputs)

