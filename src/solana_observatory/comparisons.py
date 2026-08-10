"""Deterministic, direction-neutral comparisons for daily metric series."""

from __future__ import annotations

from datetime import date, timedelta
import math
from typing import Any


def _unavailable(metric_id: str, reason: str) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "status": "unavailable",
        "grain": "daily",
        "current_average": None,
        "previous_average": None,
        "absolute_change": None,
        "percent_change": None,
        "direction": "unknown",
        "previous_window": None,
        "current_window": None,
        "reason": reason,
    }


def build_comparison(metric: dict[str, Any]) -> dict[str, Any]:
    """Compare the latest seven daily observations with the preceding seven."""

    metric_id = str(metric.get("id", "unknown"))
    series = metric.get("series")
    if not isinstance(series, list) or len(series) < 14:
        return _unavailable(metric_id, "A 14-day daily series is required.")

    observations: list[tuple[date, float]] = []
    try:
        for point in series[-14:]:
            observed_at = date.fromisoformat(point["observed_at"])
            value = float(point["value"])
            if not math.isfinite(value):
                raise ValueError
            observations.append((observed_at, value))
    except (KeyError, TypeError, ValueError):
        return _unavailable(
            metric_id, "Comparison requires finite values at a daily grain."
        )

    dates = [observed_at for observed_at, _ in observations]
    if any(
        current - previous != timedelta(days=1)
        for previous, current in zip(dates, dates[1:])
    ):
        return _unavailable(
            metric_id, "Comparison requires a contiguous daily series."
        )

    previous = observations[:7]
    current = observations[7:]
    previous_average = sum(value for _, value in previous) / 7
    current_average = sum(value for _, value in current) / 7
    absolute_change = current_average - previous_average
    if absolute_change > 0:
        direction = "increased"
    elif absolute_change < 0:
        direction = "decreased"
    else:
        direction = "flat"
    percent_change = (
        None
        if previous_average == 0
        else absolute_change / previous_average * 100
    )
    return {
        "metric_id": metric_id,
        "status": "ok",
        "grain": "daily",
        "current_average": round(current_average, 2),
        "previous_average": round(previous_average, 2),
        "absolute_change": round(absolute_change, 2),
        "percent_change": (
            None if percent_change is None else round(percent_change, 2)
        ),
        "direction": direction,
        "previous_window": [previous[0][0].isoformat(), previous[-1][0].isoformat()],
        "current_window": [current[0][0].isoformat(), current[-1][0].isoformat()],
        "reason": None,
    }


def build_comparisons(metrics: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build records only for metrics that carry historical observations."""

    return {
        metric_id: build_comparison(metric)
        for metric_id, metric in metrics.items()
        if metric.get("series")
    }
