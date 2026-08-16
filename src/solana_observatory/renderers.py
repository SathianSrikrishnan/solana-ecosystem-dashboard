"""Render one verified snapshot into the bounty's required formats."""

from __future__ import annotations

import html
import json
from datetime import date, datetime, timedelta, timezone
from typing import Any

from .comparisons import build_comparisons


SECTION_DETAILS = {
    "network": (
        "Network",
        "Live network capacity, timing, and selected RPC health.",
    ),
    "adoption": (
        "Adoption",
        "Wallet activity and retention with identity limitations kept visible.",
    ),
    "economy": (
        "Economy",
        "Market, liquidity, fees, and onchain economic activity.",
    ),
    "validators": (
        "Validators",
        "Validator participation and, in later slices, stake distribution.",
    ),
    "ecosystem": (
        "Ecosystem",
        "Selected upgrades, announcements, and application movements.",
    ),
    "financial_rails": (
        "Financial rails",
        "Tokenized assets, stablecoin settlement, payments, and liquidity.",
    ),
}

SECTION_QUESTIONS = {
    "network": "Is Solana working?",
    "adoption": "Are people and applications returning?",
    "economy": "Is useful economic activity growing?",
    "validators": "Is the network resilient and decentralized?",
    "ecosystem": "Is Solana continuing to compound?",
    "financial_rails": "Is Solana becoming real financial infrastructure?",
}

EXPECTED_EVIDENCE = {
    "network": "success rate, typical fees, and incident history",
    "adoption": "new and returning addresses, retention, app mix, and automation",
    "economy": "capital flows, app fees and revenue, chain fees, and REV",
    "validators": "stake concentration, vote participation, and client diversity",
    "ecosystem": "developer retention, active applications, upgrades, and incidents",
    "financial_rails": "RWA value, issuers, holders, liquidity, and identifiable payments",
}


def _section_anchor(section: str) -> str:
    return section.replace("_", "-")


def render_json(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, sort_keys=True) + "\n"


def _display_value(metric: dict[str, Any]) -> str:
    value = metric["value"]
    if value is None:
        return "Not available"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def _compact_display_value(metric: dict[str, Any]) -> str:
    value = metric["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return _display_value(metric)
    magnitude = abs(value)
    if magnitude >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if magnitude >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return _display_value(metric)


def _display_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is None:
        return value
    utc_value = parsed.astimezone(timezone.utc)
    return f"{utc_value.strftime('%b')} {utc_value.day}, {utc_value.year} · {utc_value:%H:%M} UTC"


def _adoption_refresh_dates(snapshot: dict[str, Any]) -> tuple[str, str]:
    source_dates = []
    for metric in snapshot.get("metrics", {}).values():
        if metric.get("source", {}).get("name") != "Dune":
            continue
        try:
            source_dates.append(date.fromisoformat(str(metric.get("source_time"))[:10]))
        except ValueError:
            continue
    if not source_dates:
        return "Not connected", "After source connection"
    verified = min(source_dates)
    next_refresh = verified + timedelta(days=3)
    display = lambda value: f"{value.strftime('%b')} {value.day}, {value.year}"
    return display(verified), display(next_refresh)


def _status_label(status: str) -> str:
    return {
        "ok": "Data reporting",
        "stale": "Data stale",
        "unavailable": "Data unavailable",
        "error": "Source failed",
        "planned": "Planned",
    }.get(status, status)


def _short_date(value: str) -> str:
    observed = date.fromisoformat(value)
    return f"{observed.strftime('%b')} {observed.day:02d}"


def _comparison_markup(comparison: dict[str, Any] | None) -> str:
    if not comparison or comparison.get("status") != "ok":
        return ""
    percent_change = comparison.get("percent_change")
    if percent_change is None:
        change = "percent change unavailable (zero baseline)"
    else:
        change = f"{percent_change:+.1f}%"
    previous = comparison["previous_window"]
    current = comparison["current_window"]
    return """
        <div class="comparison" data-direction="{direction}">
          <strong>7-day average {change}</strong>
          <span>{previous_start}–{previous_end} vs {current_start}–{current_end}</span>
          <small>Direction is not a health verdict.</small>
        </div>
    """.format(
        direction=html.escape(comparison["direction"]),
        change=html.escape(change),
        previous_start=_short_date(previous[0]),
        previous_end=_short_date(previous[1]),
        current_start=_short_date(current[0]),
        current_end=_short_date(current[1]),
    )


def _sparkline_markup(metric_id: str, metric: dict[str, Any]) -> str:
    series = metric.get("series")
    if not isinstance(series, list) or len(series) < 4:
        return ""
    values = [point.get("value") for point in series if isinstance(point, dict)]
    if len(values) != len(series) or any(
        isinstance(value, bool) or not isinstance(value, (int, float))
        for value in values
    ):
        return ""
    width, height, padding = 240, 54, 3
    low, high = min(values), max(values)
    span = high - low
    points = []
    for index, value in enumerate(values):
        x = padding + index * (width - 2 * padding) / (len(values) - 1)
        y = height / 2 if span == 0 else padding + (high - value) * (height - 2 * padding) / span
        points.append(f"{x:.1f},{y:.1f}")
    first, latest = values[0], values[-1]
    description = (
        f"{metric['label']} trend across {len(values)} observations, "
        f"from {first:,.2f} to {latest:,.2f} {metric['unit']}."
    )
    return """
        <figure class="sparkline" data-sparkline="{metric_id}">
          <svg viewBox="0 0 {width} {height}" role="img" aria-label="{description}">
            <line x1="{padding}" y1="{middle}" x2="{right}" y2="{middle}" class="spark-guide"></line>
            <polyline points="{points}" class="spark-path"></polyline>
          </svg>
          <figcaption><span>{count} observations</span><strong>{first} → {latest}</strong></figcaption>
        </figure>
    """.format(
        metric_id=html.escape(metric_id),
        width=width,
        height=height,
        padding=padding,
        middle=height / 2,
        right=width - padding,
        points=" ".join(points),
        description=html.escape(description, quote=True),
        count=len(values),
        first=f"{first:,.2f}",
        latest=f"{latest:,.2f}",
    )


def _validator_leaderboard_markup(leaderboard: dict[str, Any] | None) -> str:
    if not isinstance(leaderboard, dict) or not leaderboard.get("records"):
        return ""
    rows = []
    for record in leaderboard["records"]:
        commission = record.get("commission_pct")
        share = record.get("stake_share_pct")
        rows.append(
            """
              <tr>
                <td>{rank}</td><td><code>{vote_pubkey}</code></td>
                <td>{stake:,.2f}</td><td>{share}</td><td>{commission}</td><td>{status}</td>
              </tr>
            """.format(
                rank=record["rank"],
                vote_pubkey=html.escape(record["vote_pubkey"]),
                stake=record["activated_stake_sol"],
                share="—" if share is None else f"{share:.2f}%",
                commission="—" if commission is None else f"{commission:.2f}%",
                status=html.escape(record["status"]),
            )
        )
    return """
      <section class="leaderboard" id="validator-leaderboard" aria-labelledby="validator-leaderboard-title">
        <div class="leaderboard-heading">
          <div><span class="eyebrow">Validator depth</span><h3 id="validator-leaderboard-title">Top vote accounts by activated stake</h3></div>
          <p>{caveat}</p>
        </div>
        <div class="table-scroll" tabindex="0" aria-label="Top vote accounts table"><table>
          <thead><tr><th>Rank</th><th>Vote account</th><th>Stake (SOL)</th><th>Share</th><th>Commission</th><th>Status</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
        <p class="table-source">Source: <a href="{source_url}">{source_name}</a> / <code>{method}</code> · collected {collected_at}</p>
      </section>
    """.format(
        caveat=html.escape(leaderboard["caveat"]),
        rows="".join(rows),
        source_url=html.escape(leaderboard["source"]["url"], quote=True),
        source_name=html.escape(leaderboard["source"]["name"]),
        method=html.escape(leaderboard["source"]["method"]),
        collected_at=html.escape(leaderboard["collected_at"]),
    )


def _anomaly_monitor(snapshot: dict[str, Any]) -> str:
    anomalies = snapshot.get("anomalies", {})
    if not isinstance(anomalies, dict):
        anomalies = {}
    counts = {
        status: sum(record.get("status") == status for record in anomalies.values())
        for status in ("notable", "within_range", "unavailable")
    }
    notable_rows = []
    for metric_id, record in anomalies.items():
        if record.get("status") != "notable":
            continue
        metric = snapshot["metrics"].get(metric_id, {})
        observed = record.get("observed_change_pct")
        threshold = record.get("threshold_pct")
        notable_rows.append(
            "<li><strong>{label}</strong><span>{observed:+.1f}% · threshold {threshold:.1f}%</span></li>".format(
                label=html.escape(metric.get("label", metric_id)),
                observed=observed,
                threshold=threshold,
            )
        )
    detail = (
        "<ul>" + "".join(notable_rows) + "</ul>"
        if notable_rows
        else "<p>No monitored movement crossed its configured review threshold.</p>"
    )
    return """
      <aside class="anomaly-monitor" id="anomaly-monitor" aria-labelledby="anomaly-monitor-title">
        <div class="monitor-heading"><span class="eyebrow">Deterministic review queue</span><h2 id="anomaly-monitor-title">Anomaly monitor</h2></div>
        <div class="monitor-counts">
          <span aria-label="{notable} notable"><strong>{notable}</strong> notable</span>
          <span aria-label="{within} within range"><strong>{within}</strong> within range</span>
          <span aria-label="{unavailable} unavailable"><strong>{unavailable}</strong> unavailable</span>
        </div>
        {detail}
        <small>A threshold crossing is a review prompt, not a health verdict.</small>
      </aside>
    """.format(
        notable=counts["notable"],
        within=counts["within_range"],
        unavailable=counts["unavailable"],
        detail=detail,
    )


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

    comparisons = snapshot.get("comparisons") or build_comparisons(
        snapshot["metrics"]
    )
    for metric_id, metric in snapshot["metrics"].items():
        lines.extend(
            [
                f"### {metric['label']}: {_display_value(metric)} {metric['unit']}",
                "",
                metric["definition"],
                "",
                f"**Why it matters:** {metric['why_it_matters']}",
                "",
                f"- Status: `{metric['status']}`",
                f"- Source: {metric['source']['name']} / `{metric['source']['method']}`",
                f"- Collected: `{metric['collected_at']}`",
                f"- Confidence: `{metric['confidence']}`",
                f"- Important limitation: {metric['caveat']}",
                "",
            ]
        )
        comparison = comparisons.get(metric_id)
        if comparison and comparison.get("status") == "ok":
            percent = comparison.get("percent_change")
            change = (
                "unavailable (zero baseline)"
                if percent is None
                else f"{percent:+.1f}%"
            )
            lines.extend(
                [
                    f"- 7-day average change: `{change}`",
                    "- Direction is not a health verdict.",
                    "",
                ]
            )

    leaderboard = snapshot.get("validator_leaderboard")
    if isinstance(leaderboard, dict) and leaderboard.get("records"):
        lines.extend(
            [
                "## Top vote accounts by activated stake",
                "",
                "| Rank | Vote account | Stake (SOL) | Share | Commission | Status |",
                "|---:|---|---:|---:|---:|---|",
            ]
        )
        for record in leaderboard["records"]:
            share = record.get("stake_share_pct")
            commission = record.get("commission_pct")
            lines.append(
                "| {rank} | `{vote}` | {stake:,.2f} | {share} | {commission} | {status} |".format(
                    rank=record["rank"],
                    vote=record["vote_pubkey"],
                    stake=record["activated_stake_sol"],
                    share="—" if share is None else f"{share:.2f}%",
                    commission="—" if commission is None else f"{commission:.2f}%",
                    status=record["status"],
                )
            )
        lines.extend(["", f"**Important limitation:** {leaderboard['caveat']}", ""])

    lines.extend(
        [
            "## How to read this",
            "",
            "These measurements describe different parts of Solana. They do not, by themselves, prove how many humans are using the network or why activity changed.",
            "",
        ]
    )
    return "\n".join(lines)


def _metric_card(
    metric_id: str,
    metric: dict[str, Any],
    comparison: dict[str, Any] | None = None,
) -> str:
    return """
      <article class="metric-card" data-metric="{metric_id}" data-status="{status}">
        <div class="metric-topline">
          <span class="fact-label">Verified measurement</span>
          <span class="status status-{status}">{status_label}</span>
        </div>
        <h3>{label}</h3>
        <div class="metric-reading">
          <span class="metric-value">{value}</span>
          <span class="metric-unit">{unit}</span>
        </div>
        {sparkline}
        {comparison}
        <p class="definition"><strong>What this measures:</strong> {definition}</p>
        <details>
          <summary>Why it matters · risks · evidence</summary>
          <div class="evidence">
            <p><strong>Exact value:</strong> {exact_value} {unit}</p>
            <p><strong>Why it matters:</strong> {why_it_matters}</p>
            <p><strong>What could fool you:</strong> {caveat}</p>
            <p><strong>See the evidence:</strong> <a href="{source_url}">{source}</a> / <code>{method}</code></p>
            <p><strong>Collected:</strong> {collected_at}</p>
            <p><strong>Confidence:</strong> {confidence}</p>
          </div>
        </details>
      </article>
    """.format(
        metric_id=html.escape(metric_id),
        label=html.escape(metric["label"]),
        status=html.escape(metric["status"]),
        status_label=html.escape(_status_label(metric["status"])),
        value=html.escape(_compact_display_value(metric)),
        exact_value=html.escape(_display_value(metric)),
        unit=html.escape(metric["unit"]),
        sparkline=_sparkline_markup(metric_id, metric),
        comparison=_comparison_markup(comparison),
        definition=html.escape(metric["definition"]),
        why_it_matters=html.escape(metric["why_it_matters"]),
        source=html.escape(metric["source"]["name"]),
        source_url=html.escape(metric["source"]["url"], quote=True),
        method=html.escape(metric["source"]["method"]),
        collected_at=html.escape(metric["collected_at"]),
        confidence=html.escape(metric["confidence"]),
        caveat=html.escape(metric["caveat"]),
    )


def _signal_card(
    question: str,
    metric: dict[str, Any] | None,
) -> str:
    if metric is None:
        status = "planned"
        label = "Awaiting verified data"
        value = "Not available"
        unit = "A verified adapter will activate this signal."
    else:
        status = metric["status"]
        label = metric["label"]
        value = _compact_display_value(metric)
        unit = metric["unit"]

    return """
      <article class="signal-card">
        <div class="metric-topline">
          <span>{question}</span>
          <span class="status status-{status}">{status_label}</span>
        </div>
        <h3>{label}</h3>
        <div class="signal-value">{value}</div>
        <div class="metric-unit">{unit}</div>
      </article>
    """.format(
        question=html.escape(question),
        label=html.escape(label),
        status=html.escape(status),
        status_label=html.escape(_status_label(status)),
        value=html.escape(value),
        unit=html.escape(unit),
    )


def _analysis_panel(snapshot: dict[str, Any]) -> str:
    analysis = snapshot.get("analysis")
    if not isinstance(analysis, dict) or analysis.get("status") != "ok":
        return """
      <aside class="analysis-panel" data-status="unavailable">
        <div class="metric-topline">
          <span class="eyebrow">Automatic evidence briefing</span>
          <span class="status status-unavailable">unavailable</span>
        </div>
        <h2>Analysis unavailable for this snapshot</h2>
        <p>The verified report remains available. No explanation is generated unless a grounded analysis record is supplied by the scheduled pipeline.</p>
      </aside>
        """

    supporting_metric_ids = ", ".join(
        str(metric_id)
        for metric_id in analysis.get("supporting_metric_ids", [])
    ) or "None supplied"
    kind = str(analysis.get("kind", "ai"))
    badge = "Deterministic" if kind == "deterministic" else "Grounded"
    return """
      <aside class="analysis-panel" data-status="ok">
        <div class="metric-topline">
          <span class="eyebrow">Automatic evidence briefing</span>
          <span class="status status-ok">{badge}</span>
        </div>
        <h2>{current_reading}</h2>
        <p><strong>Uncertainty:</strong> {uncertainty}</p>
        <div class="analysis-meta">
          <span><strong>Evidence:</strong> {supporting_metric_ids}</span>
          <span><strong>Generated:</strong> {generated_at}</span>
          <span><strong>Engine:</strong> {model}</span>
        </div>
      </aside>
    """.format(
        current_reading=html.escape(str(analysis.get("current_reading", ""))),
        badge=html.escape(badge),
        uncertainty=html.escape(str(analysis.get("uncertainty", "Not supplied"))),
        supporting_metric_ids=html.escape(supporting_metric_ids),
        generated_at=html.escape(str(analysis.get("generated_at", "Not supplied"))),
        model=html.escape(str(analysis.get("model", "Not supplied"))),
    )


def _timeline_panel(timeline: list[dict[str, Any]]) -> str:
    if not timeline:
        return ""
    eras = "\n".join(
        """
        <article class="era">
          <div class="era-marker"><span>{order:02d}</span><strong>{period}</strong></div>
          <div><h3>{title}</h3><p><span>Verified historical fact</span>{fact}</p></div>
          <div><p><span>Observatory interpretation</span>{interpretation}</p><a href="{source_url}">{source_label} ↗</a></div>
        </article>
        """.format(
            order=era["order"],
            period=html.escape(era["period"]),
            title=html.escape(era["title"]),
            fact=html.escape(era["fact"]),
            interpretation=html.escape(era["interpretation"]),
            source_url=html.escape(era["source_url"], quote=True),
            source_label=html.escape(era["source_label"]),
        )
        for era in timeline
    )
    return """
    <section class="dashboard-section history" id="history">
      <div class="section-heading">
        <div><span class="section-index">07</span><div><p class="section-question">Why now?</p><h2>Seven eras of Solana</h2></div></div>
        <p>From a performance experiment to a test of global financial infrastructure. Facts and interpretation remain separate.</p>
      </div>
      <div class="history-rail">{eras}</div>
    </section>
    """.format(eras=eras)


def _activity_lens(metrics: dict[str, dict[str, Any]]) -> str:
    signers = metrics.get("daily_unique_successful_signers", {}).get("value")
    jupiter = metrics.get("daily_unique_jupiter_swap_signers", {}).get("value")
    return_rate = metrics.get("jupiter_swap_signer_7d_return_rate", {}).get("value")
    if not isinstance(signers, (int, float)) or signers <= 0:
        return ""
    jupiter_share = (
        None
        if not isinstance(jupiter, (int, float))
        else jupiter / signers * 100
    )
    return """
      <aside class="identity-lens">
        <div><span class="eyebrow">Identity and automation lens</span><h3>We cannot classify bots yet.</h3></div>
        <div class="identity-facts">
          <p><strong>{jupiter_share}</strong><span>Jupiter share of successful signers</span></p>
          <p><strong>{return_rate}</strong><span>Returning Jupiter signer rate</span></p>
        </div>
        <p><strong>Evidence still needed:</strong> transaction frequency, timing regularity, program breadth, funding relationships, and repeated instruction patterns. Addresses can be people, bots, custodians, or several wallets controlled by one person.</p>
      </aside>
    """.format(
        jupiter_share=(
            "Not available" if jupiter_share is None else f"{jupiter_share:.1f}%"
        ),
        return_rate=(
            "Not available"
            if not isinstance(return_rate, (int, float))
            else f"{return_rate:.1f}%"
        ),
    )


def render_html(snapshot: dict[str, Any]) -> str:
    metrics = snapshot["metrics"]
    comparisons = snapshot.get("comparisons") or build_comparisons(metrics)
    grouped_metrics = {
        section: [
            (metric_id, metric)
            for metric_id, metric in metrics.items()
            if metric.get("section", "network") == section
        ]
        for section in SECTION_DETAILS
    }
    section_markup = []
    for index, (section, (title, description)) in enumerate(
        SECTION_DETAILS.items(), start=1
    ):
        section_metrics = grouped_metrics[section]
        if section_metrics:
            content = '<div class="metric-grid">' + "\n".join(
                _metric_card(metric_id, metric, comparisons.get(metric_id))
                for metric_id, metric in section_metrics
            ) + "</div>"
            if section == "adoption":
                content += _activity_lens(metrics)
            if section == "validators":
                content += _validator_leaderboard_markup(
                    snapshot.get("validator_leaderboard")
                )
        else:
            content = """
              <div class="empty-state">
                <span class="status status-planned">Data adapter planned</span>
                <p>This section will activate when its verified data slice lands.</p>
                <p><strong>Expected evidence:</strong> {expected_evidence}.</p>
              </div>
            """.format(expected_evidence=EXPECTED_EVIDENCE[section])
        section_markup.append(
            """
            <section class="dashboard-section" id="{anchor}">
              <div class="section-heading">
                <div>
                  <span class="section-index">{index:02d}</span>
                  <div><p class="section-question">{question}</p><h2>{title}</h2></div>
                </div>
                <p>{description}</p>
              </div>
              {content}
            </section>
            """.format(
                anchor=_section_anchor(section),
                index=index,
                title=title,
                question=SECTION_QUESTIONS[section],
                description=description,
                content=content,
            )
        )

    signal_markup = "\n".join(
        _signal_card(
            SECTION_QUESTIONS[section],
            metrics.get("rpc_health") if section == "network" else next(
                (
                    metric
                    for _, metric in grouped_metrics[section]
                    if metric.get("status") == "ok"
                ),
                next(
                    (metric for _, metric in grouped_metrics[section]),
                    None,
                ),
            ),
        )
        for section in SECTION_DETAILS
    )
    reporting_count = sum(
        metric["status"] == "ok" for metric in metrics.values()
    )
    metric_count = len(metrics)
    gap_count = metric_count - reporting_count
    gap_label = "gap" if gap_count == 1 else "gaps"
    embedded_snapshot = json.dumps(snapshot).replace("</", "<\\/")
    dashboard_sections = "\n".join(section_markup)
    analysis_panel = _analysis_panel(snapshot)
    anomaly_monitor = _anomaly_monitor(snapshot)
    timeline_panel = _timeline_panel(snapshot.get("timeline", []))

    document = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A source-visible Solana ecosystem observatory.">
  <meta name="theme-color" content="#070a0e">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Solana Observatory">
  <meta property="og:description" content="A six-question guide to how Solana works. Every claim inspectable.">
  <meta property="og:image" content="https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/solana-observatory-cover.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Solana Observatory">
  <meta name="twitter:description" content="A six-question guide to how Solana works.">
  <meta name="twitter:image" content="https://sathiansrikrishnan.github.io/solana-ecosystem-dashboard/solana-observatory-cover.png">
  <title>Solana Ecosystem Dashboard</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #070a0e;
      --panel: #10161c;
      --panel-raised: #151d25;
      --text: #f0f5f3;
      --muted: #96a6a1;
      --line: #25312f;
      --green: #4df0a8;
      --cyan: #79c6d9;
      --violet: #a58cff;
      --amber: #f1bd67;
      --red: #ff7f75;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      overflow-x: hidden;
      touch-action: manipulation;
      background:
        linear-gradient(rgba(77,240,168,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(77,240,168,.025) 1px, transparent 1px),
        radial-gradient(circle at 75% 0%, rgba(77,240,168,.1), transparent 38rem),
        var(--bg);
      background-size: 48px 48px, 48px 48px, auto, auto;
      color: var(--text);
      font: 16px/1.55 "Segoe UI Variable", "Trebuchet MS", sans-serif;
    }}
    a {{ color: inherit; }}
    a:focus-visible, summary:focus-visible {{ outline: 2px solid var(--green); outline-offset: 4px; }}
    .skip-link {{ position: fixed; left: 16px; top: -80px; z-index: 10; padding: 10px 14px; background: var(--green); color: var(--bg); }}
    .skip-link:focus {{ top: 12px; }}
    .site-header {{ position: sticky; top: 0; z-index: 5; border-bottom: 1px solid var(--line); background: rgba(7,10,14,.88); backdrop-filter: blur(18px); }}
    .header-inner {{ width: min(1180px, calc(100% - 32px)); margin: auto; display: flex; align-items: center; justify-content: space-between; gap: 24px; min-height: 68px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 760; text-decoration: none; }}
    .brand-mark {{ width: 12px; height: 12px; border: 2px solid var(--green); transform: rotate(45deg); }}
    nav {{ display: flex; gap: 4px; overflow-x: visible; scrollbar-width: none; }}
    nav a {{ padding: 8px 7px; color: var(--muted); font-size: .74rem; text-decoration: none; white-space: nowrap; }}
    nav a:hover, nav a:focus-visible {{ color: var(--text); }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: auto; padding: 70px 0 100px; }}
    #overview {{ scroll-margin-top: 80px; }}
    .eyebrow, .fact-label, .section-index {{
      color: var(--green);
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: .75rem;
      font-weight: 750;
      letter-spacing: .13em;
      text-transform: uppercase;
    }}
    h1, h2, h3, .signal-value, .metric-value, .source-health strong {{
      font-family: Bahnschrift, "Franklin Gothic Medium", sans-serif;
      font-stretch: condensed;
    }}
    h1 {{ max-width: 850px; margin: 14px 0 20px; font-size: clamp(3rem, 8vw, 6.4rem); line-height: .9; letter-spacing: -.065em; }}
    h2, h3, p {{ margin-top: 0; }}
    .lede {{ max-width: 680px; color: var(--muted); font-size: 1.1rem; }}
    .hero-meta {{ display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 34px; color: var(--muted); font-size: .8rem; }}
    .hero-meta strong {{ color: var(--text); }}
    .freshness-bar {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px 20px; margin-top: 16px; padding: 12px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); color: var(--muted); font-size: .76rem; }}
    .freshness-bar strong {{ color: var(--text); }}
    .freshness-bar button {{ min-height: 38px; margin-left: auto; padding: 7px 12px; border: 1px solid var(--green); background: transparent; color: var(--green); font: inherit; cursor: pointer; }}
    .freshness-bar button:hover, .freshness-bar button:focus-visible {{ background: rgba(77,240,168,.08); }}
    .freshness-bar button:disabled {{ cursor: wait; opacity: .65; }}
    #refresh-message {{ flex-basis: 100%; margin: 0; color: var(--muted); }}
    .reading {{
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 24px;
      margin: 48px 0 20px;
      padding: 28px;
      border: 1px solid rgba(77,240,168,.28);
      background: linear-gradient(135deg, rgba(77,240,168,.08), rgba(16,22,28,.88));
    }}
    .reading h2 {{ margin: 8px 0 0; font-size: clamp(1.5rem, 3vw, 2.4rem); line-height: 1.12; letter-spacing: -.035em; }}
    .source-health {{ align-self: end; padding-left: 24px; border-left: 1px solid var(--line); }}
    .source-health strong {{ display: block; font-size: 1.3rem; color: var(--green); }}
    .orientation {{ display: grid; grid-template-columns: .8fr 1.2fr; gap: 28px; margin: 20px 0; padding: 26px; border: 1px solid var(--line); background: rgba(16,22,28,.72); }}
    .orientation h2 {{ margin: 7px 0 10px; font-size: 1.6rem; letter-spacing: -.035em; }}
    .orientation-copy > p {{ color: var(--muted); font-size: .9rem; }}
    .start-steps {{ display: grid; gap: 9px; margin: 18px 0 0; padding: 0; list-style: none; }}
    .start-steps li {{ padding-top: 9px; border-top: 1px solid var(--line); color: var(--text); font-size: .84rem; }}
    .asset-link {{ display: inline-block; margin-top: 18px; color: var(--green); font-size: .78rem; text-underline-offset: 4px; }}
    .system-map-wrap > p {{ margin-bottom: 14px; color: var(--muted); font-size: .8rem; }}
    .system-map {{ display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--line); border-left: 1px solid var(--line); }}
    .system-link {{ min-height: 94px; padding: 12px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); text-decoration: none; }}
    .system-link span, .system-link strong {{ display: block; }}
    .system-link span {{ color: var(--green); font: .66rem/1.2 "Cascadia Mono", Consolas, monospace; letter-spacing: .08em; }}
    .system-link strong {{ margin-top: 7px; font: 1rem/1.1 Bahnschrift, "Franklin Gothic Medium", sans-serif; }}
    .system-link small {{ display: block; margin-top: 7px; color: var(--muted); font-size: .66rem; line-height: 1.3; }}
    .system-link:hover, .system-link:focus-visible {{ background: rgba(77,240,168,.06); }}
    .state-legend {{ grid-column: 1 / -1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 2px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: .72rem; }}
    .state-legend strong {{ color: var(--text); }}
    .signal-grid, .metric-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; }}
    .signal-card {{
      padding: 20px;
      border: 1px solid var(--line);
      background: rgba(16,22,28,.72);
    }}
    .signal-value {{ margin-top: 28px; font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 780; font-variant-numeric: tabular-nums; letter-spacing: -.05em; }}
    .analysis-panel {{
      margin-top: 20px;
      padding: 26px;
      border: 1px solid rgba(165,140,255,.4);
      border-left: 3px solid var(--violet);
      background: rgba(165,140,255,.06);
    }}
    .analysis-panel h2 {{ margin: 14px 0 10px; font-size: clamp(1.35rem, 2.5vw, 2rem); }}
    .analysis-panel p {{ color: var(--muted); }}
    .analysis-meta {{ display: flex; flex-wrap: wrap; gap: 8px 22px; color: var(--muted); font-size: .78rem; }}
    .analysis-meta strong {{ color: var(--text); }}
    .anomaly-monitor {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 18px 28px; margin-top: 12px; padding: 24px; border: 1px solid var(--line); background: rgba(16,22,28,.72); }}
    .monitor-heading h2 {{ margin: 6px 0 0; font-size: 1.5rem; }}
    .monitor-counts {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; }}
    .monitor-counts span {{ padding-left: 12px; border-left: 1px solid var(--line); color: var(--muted); font-size: .72rem; }}
    .monitor-counts strong {{ display: block; color: var(--text); font: 1.5rem/1 Bahnschrift, sans-serif; }}
    .anomaly-monitor ul, .anomaly-monitor > p {{ grid-column: 1 / -1; margin: 0; color: var(--muted); }}
    .anomaly-monitor ul {{ display: grid; gap: 6px; padding: 0; list-style: none; }}
    .anomaly-monitor li {{ display: flex; justify-content: space-between; gap: 16px; }}
    .anomaly-monitor li span {{ color: var(--amber); font-family: "Cascadia Mono", Consolas, monospace; }}
    .anomaly-monitor small {{ grid-column: 1 / -1; color: var(--muted); }}
    .dashboard-section {{ padding: 74px 0 10px; scroll-margin-top: 62px; }}
    .section-heading {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: end; margin-bottom: 22px; }}
    .section-heading > div {{ display: flex; align-items: baseline; gap: 16px; }}
    .section-heading h2 {{ margin: 0; font-size: 2rem; letter-spacing: -.04em; }}
    .section-question {{ margin: 0 0 3px; color: var(--green); font-size: .82rem; font-weight: 700; }}
    .section-heading p {{ max-width: 520px; margin: 0; color: var(--muted); }}
    .metric-card {{
      min-width: 0;
      padding: 22px;
      border: 1px solid var(--line);
      background: linear-gradient(145deg, rgba(21,29,37,.95), rgba(16,22,28,.95));
    }}
    .metric-topline {{ display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: .78rem; }}
    .metric-card h3 {{ min-height: 48px; margin: 22px 0 6px; font-size: 1rem; }}
    .metric-reading {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px; }}
    .metric-value {{ font-size: 2.1rem; font-weight: 760; font-variant-numeric: tabular-nums; letter-spacing: -.045em; }}
    .metric-unit {{ color: var(--violet); font-size: .78rem; }}
    .sparkline {{ margin: 16px 0 0; padding-top: 12px; border-top: 1px solid var(--line); }}
    .sparkline svg {{ display: block; width: 100%; height: 54px; overflow: visible; }}
    .spark-guide {{ stroke: var(--line); stroke-width: 1; }}
    .spark-path {{ fill: none; stroke: var(--cyan); stroke-width: 2; vector-effect: non-scaling-stroke; }}
    .sparkline figcaption {{ display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: .7rem; }}
    .sparkline figcaption strong {{ color: var(--text); font-family: "Cascadia Mono", Consolas, monospace; }}
    .comparison {{ display: grid; gap: 2px; margin: 16px 0 0; padding: 12px 0 0; border-top: 1px solid var(--line); }}
    .comparison strong {{ color: var(--text); font-size: .88rem; }}
    .comparison span, .comparison small {{ color: var(--muted); font-size: .72rem; }}
    .comparison[data-direction="increased"] strong::before {{ content: "↑ "; color: var(--violet); }}
    .comparison[data-direction="decreased"] strong::before {{ content: "↓ "; color: var(--violet); }}
    .comparison[data-direction="flat"] strong::before {{ content: "→ "; color: var(--muted); }}
    .definition {{ min-height: 64px; margin: 18px 0; color: var(--muted); font-size: .86rem; }}
    .status {{ color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }}
    .status-ok {{ color: var(--cyan); }}
    .status-unavailable, .status-stale {{ color: var(--amber); }}
    .status-error {{ color: var(--red); }}
    details {{ color: var(--muted); font-size: .78rem; }}
    summary {{ cursor: pointer; color: var(--text); }}
    code {{ color: var(--violet); }}
    .empty-state {{ padding: 30px; border: 1px dashed var(--line); color: var(--muted); }}
    .empty-state p {{ margin: 10px 0 0; }}
    .leaderboard {{ margin-top: 18px; padding: 24px; border: 1px solid var(--line); background: rgba(16,22,28,.72); }}
    .leaderboard-heading {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: end; margin-bottom: 18px; }}
    .leaderboard-heading h3 {{ margin: 6px 0 0; font-size: 1.35rem; }}
    .leaderboard-heading p, .table-source {{ margin: 0; color: var(--muted); font-size: .78rem; }}
    .table-scroll {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .78rem; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }}
    th {{ color: var(--muted); font-size: .68rem; letter-spacing: .06em; text-transform: uppercase; }}
    th:nth-child(2), td:nth-child(2), th:last-child, td:last-child {{ text-align: left; }}
    td code {{ color: var(--text); }}
    .table-source {{ margin-top: 14px; }}
    .history-rail {{ border-top: 1px solid var(--line); }}
    .era {{ display: grid; grid-template-columns: 150px 1fr 1fr; gap: 28px; padding: 26px 0; border-bottom: 1px solid var(--line); }}
    .era-marker {{ display: grid; align-content: start; gap: 4px; font-family: "Cascadia Mono", Consolas, monospace; }}
    .era-marker span {{ color: var(--green); font-size: .7rem; }}
    .era-marker strong {{ font-size: 1.1rem; }}
    .era h3 {{ margin-bottom: 8px; font-size: 1.15rem; }}
    .era p {{ margin-bottom: 8px; color: var(--muted); font-size: .84rem; }}
    .era p span {{ display: block; margin-bottom: 4px; color: var(--text); font-size: .68rem; font-weight: 750; letter-spacing: .08em; text-transform: uppercase; }}
    .era a {{ color: var(--violet); font-size: .76rem; }}
    .learn-intro {{ max-width: 760px; margin-bottom: 24px; color: var(--muted); }}
    .learn-bridge {{ max-width: 760px; margin: -10px 0 24px; color: var(--muted); font-size: .9rem; }}
    .learn-bridge a {{ color: var(--green); font-weight: 700; text-underline-offset: 3px; }}
    .learn-guide {{ border-top: 1px solid var(--line); }}
    .learn-guide details {{ padding: 18px 0; border-bottom: 1px solid var(--line); font-size: .92rem; }}
    .learn-guide summary {{ display: flex; align-items: baseline; justify-content: space-between; gap: 20px; font-family: Bahnschrift, "Franklin Gothic Medium", sans-serif; font-size: 1.15rem; }}
    .learn-guide summary::after {{ content: "+"; color: var(--green); font-family: "Cascadia Mono", Consolas, monospace; }}
    .learn-guide details[open] summary::after {{ content: "−"; }}
    .learn-guide details > div {{ max-width: 780px; padding-top: 14px; color: var(--muted); }}
    .learn-guide strong {{ color: var(--text); }}
    .identity-lens {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px; padding: 24px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }}
    .identity-lens h3 {{ margin: 8px 0 0; font-size: 1.5rem; }}
    .identity-lens > p {{ grid-column: 1 / -1; margin: 0; color: var(--muted); font-size: .82rem; }}
    .identity-facts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .identity-facts p {{ margin: 0; }}
    .identity-facts strong, .identity-facts span {{ display: block; }}
    .identity-facts strong {{ font-family: Bahnschrift, "Franklin Gothic Medium", sans-serif; font-size: 1.6rem; }}
    .identity-facts span {{ color: var(--muted); font-size: .72rem; }}
    .methods-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .methods-card, .interpretation {{
      padding: 26px;
      border: 1px solid var(--line);
      background: rgba(16,22,28,.72);
    }}
    .interpretation {{
      border-left: 3px solid var(--violet);
      background: rgba(154,140,255,.06);
      color: var(--muted);
    }}
    @keyframes settle-in {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    #overview > * {{ animation: settle-in .55s ease-out both; }}
    #overview > :nth-child(2) {{ animation-delay: .06s; }}
    #overview > :nth-child(3) {{ animation-delay: .12s; }}
    #overview > :nth-child(4) {{ animation-delay: .18s; }}
    #overview > :nth-child(5) {{ animation-delay: .24s; }}
    #overview > :nth-child(6) {{ animation-delay: .3s; }}
    @media (max-width: 900px) {{
      .signal-grid, .metric-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
      .header-inner {{ align-items: flex-start; flex-direction: column; padding: 14px 0 10px; }}
      nav {{ width: 100%; overflow-x: auto; }}
      #overview {{ scroll-margin-top: 116px; }}
    }}
    @media (max-width: 680px) {{
      main, .header-inner {{ width: min(100% - 24px, 1180px); }}
      main {{ padding-top: 48px; }}
      .reading, .orientation, .section-heading, .methods-grid, .era, .identity-lens, .leaderboard-heading, .anomaly-monitor {{ grid-template-columns: 1fr; }}
      .source-health {{ padding: 20px 0 0; border: 0; border-top: 1px solid var(--line); }}
      .signal-grid, .metric-grid {{ grid-template-columns: 1fr; }}
      .system-map {{ grid-template-columns: repeat(2, 1fr); }}
      .state-legend {{ grid-template-columns: 1fr; }}
      .dashboard-section {{ padding-top: 58px; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
      #overview > * {{ animation: none; }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to dashboard</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="#overview"><span class="brand-mark" aria-hidden="true"></span> Solana Observatory</a>
      <nav aria-label="Dashboard sections">
        <a href="#overview">Overview</a>
        <a href="#network">Network</a>
        <a href="#adoption">Adoption</a>
        <a href="#economy">Economy</a>
        <a href="#validators">Validators</a>
        <a href="#ecosystem">Ecosystem</a>
        <a href="#financial-rails">Financial rails</a>
        <a href="#history">History</a>
        <a href="#learn">Learn</a>
        <a href="#methods">Methods</a>
      </nav>
    </div>
  </header>
  <main id="main-content">
    <section id="overview">
      <div class="eyebrow">Six questions · every claim inspectable</div>
      <h1>I want to understand<br>how Solana works.</h1>
      <p class="lede">Start with six questions. The guide below takes you through the network systematically—from whether it is working to whether it is becoming financial infrastructure. Every number includes its definition, source, freshness, and limitation.</p>
      <div class="hero-meta">
        <span><strong>Snapshot</strong> {generated_at}</span>
        <span><strong>Contract</strong> {schema_version}</span>
        <span><strong>Access</strong> Public, no account</span>
      </div>
      <div class="freshness-bar" aria-label="Adoption data freshness">
        <span><strong>Adoption verified</strong> {adoption_verified}</span>
        <span><strong>Next adoption refresh</strong> {next_adoption_refresh}</span>
        <button id="check-latest" type="button">Check for latest data</button>
        <p id="refresh-message" aria-live="polite"></p>
      </div>

      <section class="reading" aria-labelledby="current-reading">
        <div>
          <div class="eyebrow">What is happening now?</div>
          <h2 id="current-reading">{headline}</h2>
        </div>
        <div class="source-health">
          <span class="eyebrow">Source health</span>
          <strong>{reporting_count} live · {gap_count} documented {gap_label}</strong>
          <span>Gaps remain visible instead of blanking the report.</span>
        </div>
      </section>
      <section class="orientation" id="start-here" aria-labelledby="start-here-title">
        <div class="orientation-copy">
          <span class="eyebrow">Start here</span>
          <h2 id="start-here-title">A thirty-second reading path</h2>
          <p>This is an evidence map, not a score. Use it to find the question that changed, then inspect the measurement before deciding what it means.</p>
          <ol class="start-steps">
            <li><strong>1. Read the current state</strong> above.</li>
            <li><strong>2. Follow what changed</strong> in the six signals.</li>
            <li><strong>3. Inspect the evidence</strong> inside any metric.</li>
          </ol>
          <a class="asset-link" href="solana-six-question-map.png">Open the one-page guide &#8599;</a>
        </div>
        <div class="system-map-wrap">
          <p><strong>Six questions. One living system.</strong> Choose the layer you want to understand.</p>
          <div class="system-map" aria-label="Six-question dashboard map">
            <a class="system-link" href="#network"><span>01</span><strong>Network</strong><small>Is Solana working?</small></a>
            <a class="system-link" href="#adoption"><span>02</span><strong>Adoption</strong><small>Are addresses and apps returning?</small></a>
            <a class="system-link" href="#economy"><span>03</span><strong>Economy</strong><small>Is useful activity growing?</small></a>
            <a class="system-link" href="#validators"><span>04</span><strong>Validators</strong><small>Is the network resilient?</small></a>
            <a class="system-link" href="#ecosystem"><span>05</span><strong>Ecosystem</strong><small>Is Solana compounding?</small></a>
            <a class="system-link" href="#financial-rails"><span>06</span><strong>Financial rails</strong><small>Is real infrastructure emerging?</small></a>
          </div>
        </div>
        <div class="state-legend" aria-label="Data state legend">
          <span><strong>Reporting</strong> means the source returned valid data.</span>
          <span><strong>Stale</strong> means the last verified value is preserved.</span>
          <span><strong>Unavailable</strong> means no defensible live source is connected.</span>
        </div>
      </section>
      <div class="signal-grid">{signal_markup}</div>
      {analysis_panel}
      {anomaly_monitor}
    </section>

    {dashboard_sections}

    {timeline_panel}

    <section class="dashboard-section" id="learn">
      <div class="section-heading">
        <div><span class="section-index">08</span><div><p class="section-question">New to the observatory?</p><h2>Learn the instrument</h2></div></div>
        <p>A short field guide to the dashboard, the network, and the project behind it.</p>
      </div>
      <p class="learn-intro">Start with the six questions. Open a metric only when you want its definition, interpretive risk, or source. A reporting badge describes the data feed; it is not a verdict on Solana.</p>
      <p class="learn-bridge">Prefer the story before the instruments? <a href="crypto-101.html">Read the Crypto 101 companion</a>, then return here for the evidence.</p>
      <div class="learn-guide">
        <details open>
          <summary>How do I use this dashboard?</summary>
          <div>Read the six overview signals, then follow the section that changed. Compare the latest seven complete days with the prior seven, inspect companion metrics, and check the evidence before drawing a conclusion.</div>
        </details>
        <details>
          <summary>How do I learn the concepts?</summary>
          <div>Begin with Network, Adoption, and Economy. Then study Validators and Financial Rails. Each card explains what the metric measures, why it matters, and what can fool you; the history rail shows how these questions emerged.</div>
        </details>
        <details>
          <summary>Why might Solana matter?</summary>
          <div>Solana combines low transaction costs, fast execution, and an accessible builder experience with active markets, stablecoins, payments, and tokenized assets. The observatory tests that financial-rails thesis without hiding reliability, concentration, speculation, or automation risks.</div>
        </details>
        <details>
          <summary>Why was this built?</summary>
          <div>Sathian built the observatory to replace borrowed conviction with inspectable evidence while learning Solana. That learning also informs Tooth Fairy Network, a separate mainnet project for family time capsules and long-term value. Physical books and expanded incentive features are planned, not presented here as shipped.</div>
        </details>
        <details>
          <summary>What does this have to do with families?</summary>
          <div>Financial rails matter when they become dependable enough to support long-term promises. Tooth Fairy Network is Sathian's separate mainnet experiment in family time capsules and durable incentives. The Observatory is the evidence layer: it tests reliability, cost, adoption, and financial infrastructure instead of treating conviction as proof.</div>
        </details>
      </div>
    </section>

    <section class="dashboard-section" id="methods">
      <div class="section-heading">
        <div><span class="section-index">09</span><h2>Methods</h2></div>
        <p>How to read this report without mistaking a useful metric for the whole truth.</p>
      </div>
      <div class="methods-grid">
        <article class="methods-card">
          <span class="eyebrow">Verified facts</span>
          <h3>Deterministic data pipeline</h3>
          <p>Every metric retains its definition, source, collection time, confidence, and important limitation. Total TPS includes validator votes. Non-vote TPS can still include bots. Neither number equals “humans using Solana.”</p>
        </article>
        <aside class="interpretation">
          <span class="eyebrow">Interpretation</span>
          <h3>Kept separate from measurements</h3>
          <p>Automatic explanations may use only validated facts from this snapshot. Evidence IDs, uncertainty, generation time, and model stay visible; if analysis fails, the verified report still publishes.</p>
        </aside>
      </div>
    </section>
  </main>
  <script id="snapshot" type="application/json">{embedded_snapshot}</script>
  <script>
    const checkLatest = document.getElementById("check-latest");
    const refreshMessage = document.getElementById("refresh-message");
    checkLatest.addEventListener("click", async () => {{
      checkLatest.disabled = true;
      refreshMessage.textContent = "Checking the published snapshot...";
      try {{
        const response = await fetch("report.json?check=" + Date.now(), {{ cache: "no-store" }});
        if (!response.ok) throw new Error("Snapshot check failed");
        const latest = await response.json();
        const current = JSON.parse(document.getElementById("snapshot").textContent);
        if (latest.generated_at > current.generated_at) {{
          window.location.reload();
          return;
        }}
        refreshMessage.textContent = "You already have the latest verified snapshot.";
      }} catch (error) {{
        refreshMessage.textContent = "The latest snapshot could not be checked. The verified dashboard remains available.";
      }} finally {{
        checkLatest.disabled = false;
      }}
    }});
  </script>
</body>
</html>
"""
    adoption_verified, next_adoption_refresh = _adoption_refresh_dates(snapshot)
    rendered = document.format(
        generated_at=html.escape(_display_timestamp(snapshot["generated_at"])),
        schema_version=html.escape(snapshot["schema_version"]),
        headline=html.escape(snapshot["summary"]["headline"]),
        reporting_count=reporting_count,
        metric_count=metric_count,
        gap_count=gap_count,
        gap_label=gap_label,
        adoption_verified=html.escape(adoption_verified),
        next_adoption_refresh=html.escape(next_adoption_refresh),
        signal_markup=signal_markup,
        analysis_panel=analysis_panel,
        anomaly_monitor=anomaly_monitor,
        dashboard_sections=dashboard_sections,
        timeline_panel=timeline_panel,
        embedded_snapshot=embedded_snapshot,
    )
    return "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
