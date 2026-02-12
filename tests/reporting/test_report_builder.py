from fingertips_consol.models import BenchmarkClass, IndicatorResult, TrendClass
from fingertips_consol.reporting.report_builder import split_focus_and_well


def test_split_focus_and_well_assigns_expected_categories() -> None:
    focus_item = IndicatorResult(
        indicator_id=1,
        indicator_name="Smoking prevalence",
        profile_name="Wider determinants",
        area_code="E10000031",
        area_name="Warwickshire",
        latest_value=16.2,
        england_value=13.8,
        trend=TrendClass.WORSENING,
        benchmark=BenchmarkClass.WORSE_THAN_ENGLAND,
    )

    well_item = IndicatorResult(
        indicator_id=2,
        indicator_name="Vaccination uptake",
        profile_name="Healthcare",
        area_code="E10000031",
        area_name="Warwickshire",
        latest_value=91.2,
        england_value=88.1,
        trend=TrendClass.IMPROVING,
        benchmark=BenchmarkClass.BETTER_THAN_ENGLAND,
    )

    focus, doing_well = split_focus_and_well([focus_item, well_item])

    assert focus == [focus_item]
    assert doing_well == [well_item]
