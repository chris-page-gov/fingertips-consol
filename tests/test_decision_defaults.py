from fingertips_consol.decision_defaults import (
    DEFAULT_DECISIONS,
    decision_defaults_as_dict,
)


def test_decision_defaults_include_expected_top_level_sections() -> None:
    payload = decision_defaults_as_dict()
    assert set(payload.keys()) == {
        "endpoints",
        "warwickshire",
        "benchmark",
        "delivery",
        "review",
        "schedule",
        "stakeholders",
    }


def test_default_warwickshire_districts_are_five_expected_codes() -> None:
    assert DEFAULT_DECISIONS.warwickshire.district_area_codes == (
        "E07000218",
        "E07000219",
        "E07000220",
        "E07000221",
        "E07000222",
    )
