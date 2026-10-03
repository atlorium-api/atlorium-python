"""Тесты транспортного ядра на подменённом транспорте ``httpx.MockTransport``."""

from __future__ import annotations

import json
import warnings
from collections.abc import Callable

import httpx
import pytest

import atlorium
from atlorium import AsyncAtlorium, Atlorium
from atlorium._base_client import MAX_RETRY_DELAY, RequestOptions, build_query
from atlorium._response import to_raw_response_wrapper

Handler = Callable[[httpx.Request], httpx.Response]


def make_client(handler: Handler, **kwargs: object) -> tuple[Atlorium, list[float]]:
    sleeps: list[float] = []
    kwargs.setdefault("api_key", "ak_test")
    client = Atlorium(http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kwargs)  # type: ignore[arg-type]
    client._sleep = sleeps.append
    return client, sleeps


def get(client: Atlorium, path: str = "/api/test", **params: object) -> object:
    return client.request(RequestOptions(method="GET", path=path, params=params))


def test_api_key_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ATLORIUM_API_KEY", raising=False)
    with pytest.warns(atlorium.AtloriumSandboxWarning, match="демо-ключе"):
        assert Atlorium().is_sandbox
    with pytest.warns(atlorium.AtloriumSandboxWarning):
        assert Atlorium("  ").is_sandbox
    monkeypatch.setenv("ATLORIUM_API_KEY", "ak_env")
    assert not Atlorium().is_sandbox
    assert Atlorium("ak_sandbox_demo_mockdata_v1").is_sandbox


def test_explicit_keys_do_not_warn(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ATLORIUM_API_KEY", raising=False)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert Atlorium(atlorium.SANDBOX_API_KEY).is_sandbox
        client = Atlorium("ak_x")
        assert not client.with_options(timeout=5).is_sandbox
        monkeypatch.setenv("ATLORIUM_API_KEY", "ak_env")
        assert not Atlorium().is_sandbox


def test_repr_hides_key() -> None:
    client = Atlorium("ak_secret_value")
    assert "ak_secret_value" not in repr(client)
    assert "is_sandbox=False" in repr(client)


def test_headers_and_query_serialization() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    client, _ = make_client(handler, api_key="ak_test", base_url="https://example.test/")
    assert get(client, flag=True, off=False, skip=None, items=["a", "b"], n=5) == {"ok": True}
    request = seen[0]
    assert request.url.host == "example.test"
    assert request.headers["Authorization"] == "Bearer ak_test"
    assert request.headers["Accept"] == "application/json"
    assert request.headers["User-Agent"].startswith(f"atlorium-python/{atlorium.__version__} (")
    assert dict(request.url.params) == {"flag": "true", "off": "false", "items": "a,b", "n": "5"}


def test_json_body_is_utf8() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Content-Type"] == "application/json"
        return httpx.Response(200, json=json.loads(request.content))

    client, _ = make_client(handler)
    body = {"message": "Привет"}
    result = client.request(RequestOptions(method="POST", path="/api/x", json=body, has_body=True))
    assert result == body


@pytest.mark.parametrize(
    ("status", "error_class"),
    [
        (400, atlorium.ValidationError),
        (401, atlorium.AuthenticationError),
        (402, atlorium.InsufficientCreditsError),
        (403, atlorium.PermissionDeniedError),
        (404, atlorium.NotFoundError),
        (500, atlorium.ServerError),
        (501, atlorium.ServerError),
        (418, atlorium.AtloriumError),
    ],
)
def test_status_errors_are_not_retried(status: int, error_class: type[atlorium.AtloriumError]) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        body = {"error": "bad_request", "title": "t", "message": "Сообщение сервера", "balance": 1.5}
        return httpx.Response(status, json=body, headers={"X-Request-Id": "req-1"})

    client, sleeps = make_client(handler, api_key="ak_secret")
    with pytest.raises(error_class) as info:
        get(client)
    assert calls == 1
    assert sleeps == []
    error = info.value
    assert error.status == status
    assert error.request_id == "req-1"
    assert error.error_code == "bad_request"
    assert "Сообщение сервера" in str(error)
    assert "ak_secret" not in str(error)
    if isinstance(error, atlorium.InsufficientCreditsError):
        assert error.balance == 1.5


def test_plain_text_error_body() -> None:
    client, _ = make_client(lambda r: httpx.Response(400, text="Hosts parameter is required."))
    with pytest.raises(atlorium.ValidationError, match="Hosts parameter is required"):
        get(client)


def test_retries_503_then_success() -> None:
    responses = [httpx.Response(503, text="down"), httpx.Response(503, text="down"), httpx.Response(200, json=[1])]
    client, sleeps = make_client(lambda r: responses.pop(0))
    assert get(client) == [1]
    assert len(sleeps) == 2
    assert all(0 < delay <= 8 for delay in sleeps)


def test_503_error_mentions_no_charge() -> None:
    client, sleeps = make_client(lambda r: httpx.Response(503, text="down"), max_retries=1)
    with pytest.raises(atlorium.ServiceUnavailableError, match="не списываются"):
        get(client)
    assert len(sleeps) == 1


def test_403_service_not_in_account_terms() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(403, json={"error": "service_not_in_account_terms"})

    client, sleeps = make_client(handler, max_retries=3)
    with pytest.raises(atlorium.PermissionDeniedError) as info:
        get(client)
    assert calls == 1
    assert sleeps == []
    error = info.value
    assert isinstance(error, atlorium.AtloriumError)
    assert error.status == 403
    assert error.error_code == "service_not_in_account_terms"
    assert error.retry_after is None
    assert "не входит в условия вашей учётной записи" in str(error)
    assert "support@atlorium.com" in str(error)


def test_403_with_other_code_has_generic_reason() -> None:
    client, _ = make_client(lambda r: httpx.Response(403, json={"error": "forbidden", "message": "Нет доступа"}))
    with pytest.raises(atlorium.PermissionDeniedError) as info:
        get(client)
    assert str(info.value) == "HTTP 403: Доступ запрещён. Ответ сервера: Нет доступа"


@pytest.mark.parametrize("code", ["service_disabled", "maintenance"])
def test_planned_503_is_not_retried(code: str) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        body = {"error": code, "message": "Состояние сервисов: https://atlorium.com/status"}
        return httpx.Response(503, json=body, headers={"Retry-After": "30"})

    client, sleeps = make_client(handler, max_retries=3)
    with pytest.raises(atlorium.ServiceUnavailableError) as info:
        get(client)
    assert calls == 1
    assert sleeps == []
    assert info.value.error_code == code
    assert info.value.retry_after == 30.0
    assert "не списываются" in str(info.value)


def test_other_503_is_retried_until_exhausted() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, json={"error": "server_error", "message": "Источник недоступен"})

    client, sleeps = make_client(handler, max_retries=3)
    with pytest.raises(atlorium.ServiceUnavailableError):
        get(client)
    assert calls == 4
    assert len(sleeps) == 3


def test_service_unavailable_is_server_error() -> None:
    error = atlorium.ServiceUnavailableError("down", status=503)
    assert isinstance(error, atlorium.ServerError)
    assert isinstance(error, atlorium.AtloriumError)
    client, _ = make_client(lambda r: httpx.Response(503, text="down"), max_retries=0)
    with pytest.raises(atlorium.ServerError):
        get(client)


def test_503_retry_after_header_on_error() -> None:
    wait = str(int(MAX_RETRY_DELAY) + 600)
    client, sleeps = make_client(
        lambda r: httpx.Response(503, json={"error": "ServiceUnavailable"}, headers={"Retry-After": wait})
    )
    with pytest.raises(atlorium.ServiceUnavailableError) as info:
        get(client)
    assert sleeps == []  # дольше потолка не ждём: сразу исключение
    assert info.value.retry_after == float(wait)


def test_retry_after_is_on_every_status_error() -> None:
    client, _ = make_client(lambda r: httpx.Response(500, headers={"Retry-After": "7"}))
    with pytest.raises(atlorium.ServerError) as info:
        get(client)
    assert info.value.retry_after == 7.0
    assert atlorium.AtloriumError("x").retry_after is None
    assert atlorium.APIConnectionError().retry_after is None
    assert atlorium.RateLimitError("x", retry_after=2.5).retry_after == 2.5


async def test_async_planned_503_is_not_retried_but_other_503_is() -> None:
    planned = {"error": "maintenance"}
    responses = [
        httpx.Response(503, json=planned),
        httpx.Response(503, text="down"),
        httpx.Response(200, json={"ok": 1}),
        httpx.Response(403, json={"error": "service_not_in_account_terms"}),
    ]
    calls = 0
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return responses.pop(0)

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    async with http, AsyncAtlorium("ak_test", http_client=http, max_retries=3) as client:
        client._sleep = fake_sleep
        with pytest.raises(atlorium.ServiceUnavailableError):
            await client.request(RequestOptions(method="GET", path="/a"))
        assert (calls, sleeps) == (1, [])
        assert await client.request(RequestOptions(method="GET", path="/a")) == {"ok": 1}
        assert (calls, len(sleeps)) == (3, 1)
        with pytest.raises(atlorium.PermissionDeniedError):
            await client.request(RequestOptions(method="GET", path="/a"))
        assert (calls, len(sleeps)) == (4, 1)


def test_429_respects_retry_after_header() -> None:
    responses = [httpx.Response(429, headers={"Retry-After": "3"}), httpx.Response(200, json={"a": 1})]
    client, sleeps = make_client(lambda r: responses.pop(0))
    assert get(client) == {"a": 1}
    assert sleeps == [3.0]


def test_429_retry_after_from_body() -> None:
    body = {"error": "rate_limited_client", "retryAfterSeconds": 2}
    responses = [httpx.Response(429, json=body), httpx.Response(200)]
    client, sleeps = make_client(lambda r: responses.pop(0))
    assert get(client) is None
    assert sleeps == [2.0]


def test_429_long_retry_after_raises_immediately() -> None:
    wait = str(int(MAX_RETRY_DELAY) + 1)
    client, sleeps = make_client(lambda r: httpx.Response(429, headers={"Retry-After": wait}))
    with pytest.raises(atlorium.RateLimitError) as info:
        get(client)
    assert sleeps == []
    assert info.value.retry_after == float(wait)


def test_429_exhausts_retries() -> None:
    client, sleeps = make_client(lambda r: httpx.Response(429), max_retries=2)
    with pytest.raises(atlorium.RateLimitError):
        get(client)
    assert len(sleeps) == 2


def test_network_errors_are_retried_then_raised() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ConnectError("boom", request=request)

    client, sleeps = make_client(handler, max_retries=2)
    with pytest.raises(atlorium.APIConnectionError):
        get(client)
    assert calls == 3
    assert len(sleeps) == 2


def post(client: Atlorium) -> object:
    return client.request(RequestOptions(method="POST", path="/api/test", json={}, has_body=True))


@pytest.mark.parametrize(
    "error_class", [httpx.ReadTimeout, httpx.WriteTimeout, httpx.ReadError, httpx.RemoteProtocolError]
)
def test_post_is_not_retried_when_request_may_have_reached_server(error_class: type[httpx.TransportError]) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise error_class("maybe sent", request=request)

    client, sleeps = make_client(handler, max_retries=2)
    with pytest.raises(atlorium.APIConnectionError):
        post(client)
    assert calls == 1
    assert sleeps == []


@pytest.mark.parametrize("error_class", [httpx.ConnectError, httpx.ConnectTimeout])
def test_post_is_retried_when_connection_failed(error_class: type[httpx.TransportError]) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise error_class("not sent", request=request)
        return httpx.Response(200, json={"ok": True})

    client, sleeps = make_client(handler, max_retries=2)
    assert post(client) == {"ok": True}
    assert len(sleeps) == 2


def test_get_is_retried_after_read_timeout() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("slow", request=request)
        return httpx.Response(200, json={"ok": True})

    client, sleeps = make_client(handler, max_retries=2)
    assert get(client) == {"ok": True}
    assert len(sleeps) == 1


def test_post_is_retried_on_429_and_503() -> None:
    statuses = iter([429, 503, 200])
    client, sleeps = make_client(lambda r: httpx.Response(next(statuses), json={}), max_retries=2)
    assert post(client) == {}
    assert len(sleeps) == 2


def test_timeout_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    client, _ = make_client(handler, max_retries=0)
    with pytest.raises(atlorium.APITimeoutError):
        get(client)
    assert not issubclass(atlorium.APITimeoutError, TimeoutError)


def test_timeouts_per_call_and_operation_default() -> None:
    seen: list[dict[str, float]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions["timeout"])
        return httpx.Response(200, json={})

    client, _ = make_client(handler, timeout=10)
    client.request(RequestOptions(method="GET", path="/a"))
    client.request(RequestOptions(method="GET", path="/a", default_timeout=600))
    client.request(RequestOptions(method="GET", path="/a", default_timeout=600, timeout=5))
    assert [t["read"] for t in seen] == [10, 600, 5]


def test_raw_response_metadata() -> None:
    headers = {"X-Atlorium-Sandbox": "true", "X-RateLimit-Remaining": "7", "X-RateLimit-Limit": "10"}
    client, _ = make_client(lambda r: httpx.Response(200, json={"found": True}, headers=headers))
    raw = to_raw_response_wrapper(get)(client)
    assert isinstance(raw, atlorium.ApiResponse)
    assert raw.data == {"found": True}
    assert raw.status_code == 200
    assert raw.is_sandbox
    assert raw.rate_limit == atlorium.RateLimitInfo(limit=10, remaining=7, reset=None)
    # Вне обёртки режим выключен.
    assert get(client) == {"found": True}


def test_response_types() -> None:
    client, _ = make_client(lambda r: httpx.Response(200, content=b"%PDF", headers={"Content-Type": "text/csv"}))
    assert client.request(RequestOptions(method="GET", path="/a", response_type="bytes")) == b"%PDF"
    assert client.request(RequestOptions(method="GET", path="/a", response_type="auto")) == "%PDF"


def test_build_query_skips_none() -> None:
    assert build_query({"a": None, "b": 1.5}) == [("b", "1.5")]


def test_with_options_shares_connection() -> None:
    client, _ = make_client(lambda r: httpx.Response(200, json={}))
    copy = client.with_options(timeout=99, max_retries=0)
    assert copy.timeout == 99
    assert copy.max_retries == 0
    assert copy._http is client._http
    copy.close()
    assert not client._http.is_closed


async def test_async_client_retries_and_errors() -> None:
    responses = [httpx.Response(503), httpx.Response(200, json={"ok": 1}), httpx.Response(404, json={"message": "нет"})]
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    http = httpx.AsyncClient(transport=httpx.MockTransport(lambda r: responses.pop(0)))
    async with http, AsyncAtlorium("ak_test", http_client=http) as client:
        client._sleep = fake_sleep
        assert await client.request(RequestOptions(method="GET", path="/a")) == {"ok": 1}
        with pytest.raises(atlorium.NotFoundError, match="нет"):
            await client.request(RequestOptions(method="GET", path="/a"))
    assert len(sleeps) == 1
