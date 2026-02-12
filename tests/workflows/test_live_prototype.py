from fingertips_consol.models import BenchmarkClass, TrendClass
from fingertips_consol.workflows.live_prototype import (
    PrototypeConfig,
    _benchmark_from_ci,
    _benchmark_from_sig_code,
    _benchmark_with_fallback,
    _district_codes_for_run,
    _resolve_trend_marker,
    _trend_from_marker,
)


def test_trend_mapping_high_is_good() -> None:
    assert _trend_from_marker(1, polarity_id=1) == TrendClass.IMPROVING
    assert _trend_from_marker(2, polarity_id=1) == TrendClass.WORSENING


def test_trend_mapping_low_is_good() -> None:
    assert _trend_from_marker(1, polarity_id=0) == TrendClass.WORSENING
    assert _trend_from_marker(2, polarity_id=0) == TrendClass.IMPROVING


def test_resolve_trend_marker_uses_latest_comparison_fallback() -> None:
    marker = _resolve_trend_marker(
        {
            "Marker": 0,
            "MarkerForMostRecentValueComparedWithPreviousValue": 2,
        }
    )
    assert marker == 2


def test_benchmark_mapping_uses_label_text() -> None:
    labels = {
        1: "Worse",
        2: "Similar",
        3: "Better",
    }
    assert _benchmark_from_sig_code(1, labels) == BenchmarkClass.WORSE_THAN_ENGLAND
    assert _benchmark_from_sig_code(3, labels) == BenchmarkClass.BETTER_THAN_ENGLAND
    assert _benchmark_from_sig_code(2, labels) == BenchmarkClass.SIMILAR_TO_ENGLAND


def test_ci_benchmark_fallback_when_high_is_good() -> None:
    local = {"LoCI": 82.0, "UpCI": 83.0}
    england = {"LoCI": 79.0, "UpCI": 80.0}
    assert _benchmark_from_ci(local, england, polarity_id=1) == BenchmarkClass.BETTER_THAN_ENGLAND


def test_ci_benchmark_fallback_when_low_is_good() -> None:
    local = {"LoCI": 10.0, "UpCI": 11.0}
    england = {"LoCI": 14.0, "UpCI": 15.0}
    assert _benchmark_from_ci(local, england, polarity_id=0) == BenchmarkClass.BETTER_THAN_ENGLAND


def test_benchmark_with_fallback_prefers_sig_when_available() -> None:
    benchmark, source = _benchmark_with_fallback(
        local_row={"Sig": {"4": 1}, "LoCI": 1.0, "UpCI": 2.0},
        england_row={"LoCI": 10.0, "UpCI": 11.0},
        polarity_id=1,
        sig_labels={1: "Worse", 2: "Similar", 3: "Better"},
    )
    assert benchmark == BenchmarkClass.WORSE_THAN_ENGLAND
    assert source == "sig"


def test_district_codes_for_run_prefers_canonical_with_validation() -> None:
    area_names = {
        "E10000031": "Warwickshire",
        "E92000001": "England",
        "E07000218": "North Warwickshire",
        "E07000219": "Nuneaton and Bedworth",
        "E07000220": "Rugby",
        "E07000221": "Stratford-on-Avon",
        "E07000222": "Warwick",
        "E07000999": "Unexpected district",
    }
    district_codes, missing, extra = _district_codes_for_run(area_names, PrototypeConfig())
    assert district_codes == {
        "E07000218",
        "E07000219",
        "E07000220",
        "E07000221",
        "E07000222",
    }
    assert missing == []
    assert extra == ["E07000999"]


def test_district_codes_for_run_can_skip_canonical_validation() -> None:
    area_names = {
        "E10000031": "Warwickshire",
        "E92000001": "England",
        "E07000218": "North Warwickshire",
        "E07000999": "Unexpected district",
    }
    config = PrototypeConfig(validate_district_area_codes=False)
    district_codes, missing, extra = _district_codes_for_run(area_names, config)
    assert district_codes == {"E07000218", "E07000999"}
    assert missing == []
    assert extra == []
