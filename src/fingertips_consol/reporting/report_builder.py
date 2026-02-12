"""Build report content from analyzed indicators."""

from __future__ import annotations

from datetime import datetime

from fingertips_consol.models import BenchmarkClass, IndicatorResult, TrendClass


def split_focus_and_well(
    results: list[IndicatorResult],
) -> tuple[list[IndicatorResult], list[IndicatorResult]]:
    focus: list[IndicatorResult] = []
    doing_well: list[IndicatorResult] = []

    for item in results:
        requires_focus = (
            item.trend == TrendClass.WORSENING
            or item.benchmark == BenchmarkClass.WORSE_THAN_ENGLAND
        )
        if requires_focus:
            focus.append(item)
            continue

        if (
            item.trend == TrendClass.IMPROVING
            or item.benchmark == BenchmarkClass.BETTER_THAN_ENGLAND
        ):
            doing_well.append(item)

    return focus, doing_well


def build_markdown_report(
    title: str,
    generated_at: datetime,
    items: list[IndicatorResult],
) -> str:
    lines = [
        f"# {title}",
        "",
        f"Generated: {generated_at.isoformat()}",
        "",
    ]

    if not items:
        lines.append("No indicators in this category.")
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "| Indicator | Profile | Area | Latest | England | Trend | Benchmark |",
            "|---|---|---:|---:|---:|---|---|",
        ]
    )

    for item in items:
        lines.append(
            "| "
            f"{item.indicator_name} | "
            f"{item.profile_name} | "
            f"{item.area_name} | "
            f"{item.latest_value:.2f} | "
            f"{item.england_value:.2f} | "
            f"{item.trend.value} | "
            f"{item.benchmark.value} |"
        )

    lines.append("")
    return "\n".join(lines)
