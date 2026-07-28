"""Render one verified snapshot into the bounty's required formats."""

from __future__ import annotations

import html
import json
from typing import Any


def render_json(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, sort_keys=True) + "\n"


def _display_value(metric: dict[str, Any]) -> str:
    value = metric["value"]
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        "# Solana Ecosystem Report",
        "",
        f"Generated: `{snapshot['generated_at']}`",
        "",
        f"**Current reading:** {snapshot['summary']['headline']}",
        "",
        "## What is happening now?",
        "",
    ]

    for metric in snapshot["metrics"].values():
        lines.extend(
            [
                f"### {metric['label']}: {_display_value(metric)} {metric['unit']}",
                "",
                metric["definition"],
                "",
                f"- Status: `{metric['status']}`",
                f"- Source: {metric['source']['name']} / `{metric['source']['method']}`",
                f"- Collected: `{metric['collected_at']}`",
                f"- Confidence: `{metric['confidence']}`",
                f"- Important limitation: {metric['caveat']}",
                "",
            ]
        )

    lines.extend(
        [
            "## How to read this",
            "",
            "These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.",
            "",
        ]
    )
    return "\n".join(lines)


def render_html(snapshot: dict[str, Any]) -> str:
    cards = []
    for metric_id, metric in snapshot["metrics"].items():
        cards.append(
            """
            <article class="metric-card" data-metric="{metric_id}">
              <div class="metric-topline">
                <span class="metric-label">{label}</span>
                <span class="status">{status}</span>
              </div>
              <div class="metric-value">{value}</div>
              <div class="metric-unit">{unit}</div>
              <p class="definition">{definition}</p>
              <details>
                <summary>Source and limitation</summary>
                <p><strong>Source:</strong> {source} / {method}</p>
                <p>{caveat}</p>
              </details>
            </article>
            """.format(
                metric_id=html.escape(metric_id),
                label=html.escape(metric["label"]),
                status=html.escape(metric["status"]),
                value=html.escape(_display_value(metric)),
                unit=html.escape(metric["unit"]),
                definition=html.escape(metric["definition"]),
                source=html.escape(metric["source"]["name"]),
                method=html.escape(metric["source"]["method"]),
                caveat=html.escape(metric["caveat"]),
            )
        )

    embedded_snapshot = json.dumps(snapshot).replace("</", "<\\/")
    card_markup = "\n".join(cards)
    generated_at = html.escape(snapshot["generated_at"])
    headline = html.escape(snapshot["summary"]["headline"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Solana Ecosystem Dashboard</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #090b10;
      --panel: #11151d;
      --panel-2: #171c26;
      --text: #f5f7fb;
      --muted: #9da8b8;
      --line: #273042;
      --green: #58e6a9;
      --violet: #9a8cff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at 15% 0%, rgba(88,230,169,.12), transparent 36rem),
        radial-gradient(circle at 85% 5%, rgba(154,140,255,.12), transparent 30rem),
        var(--bg);
      color: var(--text);
      font: 16px/1.55 Inter, ui-sans-serif, system-ui, sans-serif;
    }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: auto; padding: 56px 0 80px; }}
    .eyebrow {{
      color: var(--green);
      font-size: .75rem;
      font-weight: 750;
      letter-spacing: .13em;
      text-transform: uppercase;
    }}
    h1 {{ max-width: 780px; margin: 10px 0 14px; font-size: clamp(2.3rem, 7vw, 5.4rem); line-height: .95; letter-spacing: -.055em; }}
    .lede {{ max-width: 700px; color: var(--muted); font-size: 1.08rem; }}
    .reading {{
      margin: 34px 0 18px;
      padding: 22px;
      border: 1px solid rgba(88,230,169,.26);
      border-radius: 18px;
      background: rgba(17,21,29,.78);
    }}
    .reading strong {{ color: var(--green); }}
    .timestamp {{ color: var(--muted); font-size: .83rem; }}
    h2 {{ margin: 42px 0 16px; font-size: 1.35rem; letter-spacing: -.02em; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }}
    .metric-card {{
      min-height: 270px;
      padding: 20px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: linear-gradient(145deg, rgba(23,28,38,.94), rgba(17,21,29,.94));
    }}
    .metric-topline {{ display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: .78rem; }}
    .status {{ color: var(--green); text-transform: uppercase; letter-spacing: .08em; }}
    .metric-value {{ margin-top: 22px; font-size: 2.2rem; font-weight: 760; letter-spacing: -.04em; }}
    .metric-unit {{ color: var(--violet); font-size: .78rem; }}
    .definition {{ min-height: 64px; color: var(--muted); font-size: .86rem; }}
    details {{ color: var(--muted); font-size: .78rem; }}
    summary {{ cursor: pointer; color: var(--text); }}
    .explanation {{
      max-width: 780px;
      padding: 24px;
      border-left: 3px solid var(--violet);
      background: rgba(154,140,255,.06);
      color: var(--muted);
    }}
    @media (max-width: 820px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }} }}
    @media (max-width: 560px) {{
      main {{ width: min(100% - 22px, 1120px); padding-top: 32px; }}
      .grid {{ grid-template-columns: 1fr; }}
      .metric-card {{ min-height: 0; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Live foundation · direct RPC</div>
    <h1>Solana, without the fog.</h1>
    <p class="lede">A source-visible view of network health. This first build deliberately separates network machinery from claims about people or adoption.</p>

    <section class="reading">
      <div class="eyebrow">Current reading</div>
      <p><strong>{headline}</strong></p>
      <div class="timestamp">Collected {generated_at}</div>
    </section>

    <h2>What is happening now?</h2>
    <section class="grid">{card_markup}</section>

    <h2>How to read this</h2>
    <section class="explanation">
      These measurements describe the network's machinery. Total TPS includes validator votes. Non-vote TPS can still include bots. Neither number equals “humans using Solana.”
    </section>
  </main>
  <script id="snapshot" type="application/json">{embedded_snapshot}</script>
</body>
</html>
"""

