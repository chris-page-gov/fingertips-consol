from fingertips_consol.config import load_settings
from fingertips_consol.decision_defaults import DEFAULT_DECISIONS


def test_load_settings_uses_canonical_district_defaults_when_env_not_set(monkeypatch) -> None:
    monkeypatch.delenv("DISTRICT_AREA_CODES", raising=False)
    monkeypatch.delenv("WARWICKSHIRE_AREA_CODE", raising=False)

    settings = load_settings()

    assert settings.warwickshire_area_code == DEFAULT_DECISIONS.warwickshire.county_area_code
    assert settings.district_area_codes == DEFAULT_DECISIONS.warwickshire.district_area_codes


def test_load_settings_prefers_env_district_codes(monkeypatch) -> None:
    monkeypatch.setenv("DISTRICT_AREA_CODES", "X1, X2")

    settings = load_settings()

    assert settings.district_area_codes == ("X1", "X2")
