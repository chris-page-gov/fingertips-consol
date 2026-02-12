"""Trend classification utilities."""

from __future__ import annotations

from fingertips_consol.models import TrendClass


def classify_trend(
    current_value: float,
    previous_value: float,
    improvement_direction: str,
    tolerance: float = 0.0,
) -> TrendClass:
    if tolerance < 0:
        raise ValueError("tolerance must be >= 0")

    direction = improvement_direction.strip().lower()
    if direction not in {"up", "down"}:
        raise ValueError("improvement_direction must be 'up' or 'down'")

    delta = current_value - previous_value
    if abs(delta) <= tolerance:
        return TrendClass.STABLE

    if direction == "up":
        return TrendClass.IMPROVING if delta > 0 else TrendClass.WORSENING

    return TrendClass.IMPROVING if delta < 0 else TrendClass.WORSENING
