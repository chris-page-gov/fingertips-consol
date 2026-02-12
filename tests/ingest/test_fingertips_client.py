from __future__ import annotations

from typing import Any

import httpx
import pytest

from fingertips_consol.ingest.fingertips_client import FingertipsClient


def test_get_json_calls_expected_url_and_params(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    class DummyResponse:
        def raise_for_status(self) -> None:
            captured["raise_for_status_called"] = True

        def json(self) -> dict[str, str]:
            return {"ok": "yes"}

    def fake_get(url: str, params: dict[str, Any] | None, timeout: float) -> DummyResponse:
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr("fingertips_consol.ingest.fingertips_client.httpx.get", fake_get)
    client = FingertipsClient(base_url="https://example.test/api/")

    payload = client._get_json("/profiles", params={"a": 1})

    assert payload == {"ok": "yes"}
    assert captured == {
        "url": "https://example.test/api/profiles",
        "params": {"a": 1},
        "timeout": 30.0,
        "raise_for_status_called": True,
    }


def test_get_profiles_returns_empty_list_for_non_list_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FingertipsClient()
    monkeypatch.setattr(client, "_get_json", lambda path, params=None: {"profiles": []})

    profiles = client.get_profiles()

    assert profiles == []


def test_get_indicators_passes_profile_id_and_returns_list(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    client = FingertipsClient()

    def fake_get_json(path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        captured["path"] = path
        captured["params"] = params
        return [{"indicator_id": 1}]

    monkeypatch.setattr(client, "_get_json", fake_get_json)

    indicators = client.get_indicators(profile_id=11)

    assert indicators == [{"indicator_id": 1}]
    assert captured == {"path": "indicators", "params": {"profile_id": 11}}


def test_get_indicator_data_returns_empty_list_for_non_list_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    client = FingertipsClient()

    def fake_get_json(path: str, params: dict[str, Any] | None = None) -> dict[str, str]:
        captured["path"] = path
        captured["params"] = params
        return {"error": "unexpected"}

    monkeypatch.setattr(client, "_get_json", fake_get_json)

    indicator_data = client.get_indicator_data(indicator_id=99, area_code="E10000031")

    assert indicator_data == []
    assert captured == {
        "path": "data",
        "params": {"indicator_id": 99, "area_code": "E10000031"},
    }
def test_client_retries_on_http_500(monkeypatch: pytest.MonkeyPatch) -> None:
    request = httpx.Request("GET", "https://fingertips.phe.org.uk/api/profiles")
    responses = [
        httpx.Response(500, request=request, json={"error": "server"}),
        httpx.Response(200, request=request, json=[]),
    ]

    def fake_get(*args, **kwargs):  # type: ignore[no-untyped-def]
        return responses.pop(0)

    monkeypatch.setattr(httpx, "get", fake_get)
    monkeypatch.setattr("time.sleep", lambda *_: None)

    client = FingertipsClient(max_retries=2)
    assert client.get_profiles() == []


def test_client_retries_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    request = httpx.Request("GET", "https://fingertips.phe.org.uk/api/profiles")
    calls = {"count": 0}

    def fake_get(*args, **kwargs):  # type: ignore[no-untyped-def]
        calls["count"] += 1
        if calls["count"] == 1:
            raise httpx.TimeoutException("timeout")
        return httpx.Response(200, request=request, json=[])

    monkeypatch.setattr(httpx, "get", fake_get)
    monkeypatch.setattr("time.sleep", lambda *_: None)

    client = FingertipsClient(max_retries=2)
    assert client.get_profiles() == []


def test_client_does_not_retry_on_404(monkeypatch: pytest.MonkeyPatch) -> None:
    request = httpx.Request("GET", "https://fingertips.phe.org.uk/api/profiles")

    def fake_get(*args, **kwargs):  # type: ignore[no-untyped-def]
        return httpx.Response(404, request=request, json={"error": "not found"})

    monkeypatch.setattr(httpx, "get", fake_get)
    monkeypatch.setattr("time.sleep", lambda *_: None)

    client = FingertipsClient(max_retries=2)
    with pytest.raises(httpx.HTTPStatusError):
        client.get_profiles()
