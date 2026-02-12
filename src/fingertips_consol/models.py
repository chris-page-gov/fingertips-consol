"""Core models used across ingestion, analysis, and reporting."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TrendClass(StrEnum):
    IMPROVING = "improving"
    WORSENING = "worsening"
    STABLE = "stable"


class BenchmarkClass(StrEnum):
    BETTER_THAN_ENGLAND = "better_than_england"
    WORSE_THAN_ENGLAND = "worse_than_england"
    SIMILAR_TO_ENGLAND = "similar_to_england"


@dataclass(frozen=True)
class IndicatorResult:
    indicator_id: int
    indicator_name: str
    profile_name: str
    area_code: str
    area_name: str
    latest_value: float
    england_value: float
    trend: TrendClass
    benchmark: BenchmarkClass
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "IndicatorResult":
        return cls(
            indicator_id=int(row["indicator_id"]),
            indicator_name=str(row["indicator_name"]),
            profile_name=str(row.get("profile_name", "Unassigned")),
            area_code=str(row["area_code"]),
            area_name=str(row["area_name"]),
            latest_value=float(row["latest_value"]),
            england_value=float(row["england_value"]),
            trend=TrendClass(str(row["trend"])),
            benchmark=BenchmarkClass(str(row["benchmark"])),
            notes=list(row.get("notes", [])),
        )
