"""Thin client for the Fingertips API."""

from __future__ import annotations

import time
from typing import Any

import httpx


class FingertipsClient:
    def __init__(
        self,
        base_url: str = "https://fingertips.phe.org.uk/api",
        *,
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        retry_backoff_seconds: float = 0.5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds

    @staticmethod
    def _should_retry_status(status_code: int) -> bool:
        return status_code == 429 or status_code >= 500

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_exception: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = httpx.get(url, params=params, timeout=self.timeout_seconds)
                if self._should_retry_status(response.status_code) and attempt < self.max_retries:
                    delay = self.retry_backoff_seconds * (2**attempt)
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException as exc:
                last_exception = exc
                if attempt >= self.max_retries:
                    raise
                delay = self.retry_backoff_seconds * (2**attempt)
                time.sleep(delay)
            except httpx.HTTPStatusError as exc:
                last_exception = exc
                status_code = exc.response.status_code
                if not self._should_retry_status(status_code) or attempt >= self.max_retries:
                    raise
                delay = self.retry_backoff_seconds * (2**attempt)
                time.sleep(delay)

        if last_exception is not None:
            raise last_exception
        raise RuntimeError("Request failed without raising an explicit exception")

    @staticmethod
    def _csv(values: list[int] | list[str]) -> str:
        return ",".join(str(value) for value in values)

    def get_profiles(self) -> list[dict[str, Any]]:
        payload = self._get_json("profiles")
        return payload if isinstance(payload, list) else []

    def get_profile_by_key(self, profile_key: str) -> dict[str, Any]:
        payload = self._get_json("profile/by_key", params={"profile_key": profile_key})
        return payload if isinstance(payload, dict) else {}

    def get_group_metadata(self, group_ids: list[int]) -> list[dict[str, Any]]:
        payload = self._get_json(
            "group_metadata",
            params={"group_ids": self._csv(group_ids)},
        )
        return payload if isinstance(payload, list) else []

    def get_indicator_metadata_by_group_ids(self, group_ids: list[int]) -> dict[str, Any]:
        payload = self._get_json(
            "indicator_metadata/by_group_id",
            params={"group_ids": self._csv(group_ids)},
        )
        return payload if isinstance(payload, dict) else {}

    def get_areas_by_parent_area_code(
        self,
        area_type_id: int,
        parent_area_code: str,
        profile_id: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "area_type_id": area_type_id,
            "parent_area_code": parent_area_code,
        }
        if profile_id is not None:
            params["profile_id"] = profile_id
        payload = self._get_json("areas/by_parent_area_code", params=params)
        return payload if isinstance(payload, list) else []

    def get_areas_by_area_code(self, area_codes: list[str]) -> list[dict[str, Any]]:
        payload = self._get_json(
            "areas/by_area_code",
            params={"area_codes": self._csv(area_codes)},
        )
        return payload if isinstance(payload, list) else []

    def get_comparator_significances(self, polarity_id: int) -> list[dict[str, Any]]:
        payload = self._get_json(
            "comparator_significances",
            params={"polarity_id": polarity_id},
        )
        return payload if isinstance(payload, list) else []

    def get_latest_data_for_child_areas(
        self,
        *,
        area_type_id: int,
        parent_area_code: str,
        indicator_ids: list[int],
        profile_id: int,
    ) -> list[dict[str, Any]]:
        payload = self._get_json(
            "latest_data/specific_indicators_for_child_areas",
            params={
                "area_type_id": area_type_id,
                "parent_area_code": parent_area_code,
                "indicator_ids": self._csv(indicator_ids),
                "profile_id": profile_id,
            },
        )
        return payload if isinstance(payload, list) else []

    def get_latest_data_for_single_area(
        self,
        *,
        area_type_id: int,
        area_code: str,
        indicator_ids: list[int],
        restrict_to_profile_ids: list[int] | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "area_type_id": area_type_id,
            "area_code": area_code,
            "indicator_ids": self._csv(indicator_ids),
        }
        if restrict_to_profile_ids:
            params["restrict_to_profile_ids"] = self._csv(restrict_to_profile_ids)
        payload = self._get_json("latest_data/specific_indicators_for_single_area", params=params)
        return payload if isinstance(payload, list) else []
