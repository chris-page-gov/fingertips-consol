import httpx
import pytest

from fingertips_consol.ingest.fingertips_client import FingertipsClient


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
