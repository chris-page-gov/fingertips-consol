"""Helpers for grouping focus items for team-specific notification sections."""

from __future__ import annotations

from collections import defaultdict

from fingertips_consol.models import IndicatorResult


def group_focus_by_profile(results: list[IndicatorResult]) -> dict[str, list[IndicatorResult]]:
    grouped: dict[str, list[IndicatorResult]] = defaultdict(list)
    for item in results:
        grouped[item.profile_name].append(item)
    return dict(grouped)
