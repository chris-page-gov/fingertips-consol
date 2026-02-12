"""Thin client for the Fingertips API."""

from __future__ import annotations

from typing import Any

import httpx


class FingertipsClient:
    def __init__(self, base_url: str = "https://fingertips.phe.org.uk/api") -> None:
        self.base_url = base_url.rstrip("/")

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = httpx.get(f"{self.base_url}/{path.lstrip('/')}", params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()

    def get_profiles(self) -> list[dict[str, Any]]:
        payload = self._get_json("profiles")
        return payload if isinstance(payload, list) else []

    def get_indicators(self, profile_id: int | None = None) -> list[dict[str, Any]]:
        params = {"profile_id": profile_id} if profile_id is not None else None
        payload = self._get_json("indicators", params=params)
        return payload if isinstance(payload, list) else []

    def get_indicator_data(self, indicator_id: int, area_code: str) -> list[dict[str, Any]]:
        params = {"indicator_id": indicator_id, "area_code": area_code}
        payload = self._get_json("data", params=params)
        return payload if isinstance(payload, list) else []
