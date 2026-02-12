from __future__ import annotations

import pytest

from fingertips_consol.config import load_settings


def test_load_settings_uses_defaults_when_environment_not_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("FINGERTIPS_API_BASE_URL", raising=False)
    monkeypatch.delenv("WARWICKSHIRE_AREA_CODE", raising=False)
    monkeypatch.delenv("DISTRICT_AREA_CODES", raising=False)

    settings = load_settings()

    assert settings.fingertips_api_base_url == "https://fingertips.phe.org.uk/api"
    assert settings.warwickshire_area_code == "E10000031"
    assert settings.district_area_codes == ()


def test_load_settings_reads_and_strips_environment_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FINGERTIPS_API_BASE_URL", "https://example.test/api")
    monkeypatch.setenv("WARWICKSHIRE_AREA_CODE", "E12345678")
    monkeypatch.setenv("DISTRICT_AREA_CODES", " E07000170, ,E07000171 ,E07000172 ")

    settings = load_settings()

    assert settings.fingertips_api_base_url == "https://example.test/api"
    assert settings.warwickshire_area_code == "E12345678"
    assert settings.district_area_codes == ("E07000170", "E07000171", "E07000172")
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
