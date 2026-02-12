"""Workflow entrypoints for routine and on-demand reports."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fingertips_consol.models import IndicatorResult
from fingertips_consol.reporting.report_builder import build_markdown_report, split_focus_and_well


def build_results_from_payload(payload: list[dict[str, Any]]) -> list[IndicatorResult]:
    return [IndicatorResult.from_mapping(row) for row in payload]


def generate_reports(
    results: list[IndicatorResult],
    output_dir: Path,
    generated_at: datetime | None = None,
) -> dict[str, Path]:
    report_time = generated_at or datetime.now(timezone.utc)
    focus, doing_well = split_focus_and_well(results)

    output_dir.mkdir(parents=True, exist_ok=True)

    focus_path = output_dir / "focus-report.md"
    well_path = output_dir / "doing-well-report.md"

    focus_path.write_text(
        build_markdown_report("Indicators Requiring Focus", report_time, focus),
        encoding="utf-8",
    )
    well_path.write_text(
        build_markdown_report("Indicators Doing Well", report_time, doing_well),
        encoding="utf-8",
    )

    return {"focus": focus_path, "doing_well": well_path}
