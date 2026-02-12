"""Configuration helpers for environment-driven settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    fingertips_api_base_url: str
    warwickshire_area_code: str
    district_area_codes: tuple[str, ...]


def load_settings() -> Settings:
    district_codes = tuple(
        code.strip() for code in os.getenv("DISTRICT_AREA_CODES", "").split(",") if code.strip()
    )
    return Settings(
        fingertips_api_base_url=os.getenv(
            "FINGERTIPS_API_BASE_URL", "https://fingertips.phe.org.uk/api"
        ),
        warwickshire_area_code=os.getenv("WARWICKSHIRE_AREA_CODE", "E10000031"),
        district_area_codes=district_codes,
    )
