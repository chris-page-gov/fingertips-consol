from __future__ import annotations

from fingertips_consol.models import BenchmarkClass, IndicatorResult, TrendClass
from fingertips_consol.notifications.highlights import group_focus_by_profile


def _result(indicator_id: int, profile_name: str) -> IndicatorResult:
    return IndicatorResult(
        indicator_id=indicator_id,
        indicator_name=f"Indicator {indicator_id}",
        profile_name=profile_name,
        area_code="E10000031",
        area_name="Warwickshire",
        latest_value=10.0,
        england_value=9.0,
        trend=TrendClass.WORSENING,
        benchmark=BenchmarkClass.WORSE_THAN_ENGLAND,
    )


def test_group_focus_by_profile_groups_by_profile_name() -> None:
    grouped = group_focus_by_profile(
        [_result(1, "Wider determinants"), _result(2, "Healthcare"), _result(3, "Healthcare")]
    )

    assert set(grouped.keys()) == {"Wider determinants", "Healthcare"}
    assert grouped["Wider determinants"][0].indicator_id == 1
    assert [item.indicator_id for item in grouped["Healthcare"]] == [2, 3]


def test_group_focus_by_profile_returns_empty_dict_for_empty_input() -> None:
    assert group_focus_by_profile([]) == {}
