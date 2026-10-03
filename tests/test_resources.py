"""
Тесты ресурсов на подменённом транспорте: каждый из 59 методов — в синхронном и асинхронном
клиенте, плюс особые случаи (PDF, CSV, изображения, таймауты операций, метаданные ответа).

Таблица ``CASES`` написана руками, независимо от генератора: она проверяет, что
сгенерированный код шлёт ровно тот запрос, который ждёт сервер.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
import pytest

import atlorium
from atlorium import AsyncAtlorium, Atlorium
from atlorium._files import encode_image
from atlorium.types import aichat, cron, dns, egrul, testdata
from atlorium.types.cron import CronTemplateType, DayOfWeek

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PNG = FIXTURES / "white.png"
NO_BODY: Any = object()


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def load_fixture(name: str) -> Any:
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Case:
    resource: str
    method: str
    http: str
    route: str
    """Маршрут как в спеке — для сверки покрытия."""
    path: str
    """Фактический (раскодированный) путь запроса."""
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
    query: dict[str, str] = field(default_factory=dict)
    body: Any = NO_BODY

    @property
    def id(self) -> str:
        return f"{self.resource}.{self.method}"


CASES: list[Case] = [
    # ЕГРЮЛ
    Case("egrul", "get", "GET", "/api/egrul/{query}", "/api/egrul/7707083893", ("7707083893",),
         {"extended": True}, {"extended": "true"}),
    Case("egrul", "search", "GET", "/api/egrul/search", "/api/egrul/search", ("Сбербанк",), {"limit": 5},
         {"query": "Сбербанк", "limit": "5"}),
    Case("egrul", "get_excerpt", "GET", "/api/egrul/{query}/excerpt", "/api/egrul/7707083893/excerpt", ("7707083893",)),
    # БИК
    Case("cbr", "get", "GET", "/api/cbr/{bik}", "/api/cbr/044525225", ("044525225",)),
    Case("cbr", "search", "GET", "/api/cbr/search", "/api/cbr/search", ("Сбер",), {"limit": 3},
         {"query": "Сбер", "limit": "3"}),
    Case("cbr", "get_stats", "GET", "/api/cbr/stats", "/api/cbr/stats"),
    # SWIFT
    Case("swift", "get", "GET", "/api/swift/{bic}", "/api/swift/SABRRUMM", ("SABRRUMM",)),
    Case("swift", "search", "GET", "/api/swift/search", "/api/swift/search", ("Sberbank",), {},
         {"query": "Sberbank"}),
    Case("swift", "validate", "GET", "/api/swift/validate/{bic}", "/api/swift/validate/SABRRUMMXXX", ("SABRRUMMXXX",)),
    Case("swift", "get_stats", "GET", "/api/swift/stats", "/api/swift/stats"),
    # BIN
    Case("bin", "lookup", "GET", "/api/bin/{bin}", "/api/bin/424242", ("424242",), {"customer_ip": "8.8.8.8"},
         {"customerIp": "8.8.8.8"}),
    Case("bin", "validate", "GET", "/api/bin/validate/{bin}", "/api/bin/validate/424242", ("424242",)),
    # AML
    Case("aml", "screen", "POST", "/api/aml/screen", "/api/aml/screen", ("TXyz", "TRX"),
         body={"walletAddress": "TXyz", "blockchain": "TRX"}),
    Case("aml", "validate", "GET", "/api/aml/validate", "/api/aml/validate", ("TXyz", "TRX"), {},
         {"walletAddress": "TXyz", "blockchain": "TRX"}),
    # IP
    Case("ipinfo", "lookup", "GET", "/api/ipinfo/{ip}", "/api/ipinfo/8.8.8.8", ("8.8.8.8",), {"extended": False},
         {"extended": "false"}),
    # ГАР
    Case("gar", "search", "GET", "/api/gar/search", "/api/gar/search", ("Москва Тверская",), {"limit": 2},
         {"query": "Москва Тверская", "limit": "2"}),
    Case("gar", "suggest", "GET", "/api/gar/suggest", "/api/gar/suggest", ("Твер",), {}, {"query": "Твер"}),
    Case("gar", "get_object", "GET", "/api/gar/object/{guid}", "/api/gar/object/0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
         ("0c5b2444-70a0-4932-980c-b4dc0d3f02b5",)),
    Case("gar", "get_object_by_id", "GET", "/api/gar/object/id/{objectId}", "/api/gar/object/id/1234567", (1234567,)),
    Case("gar", "get_children", "GET", "/api/gar/children/{parentObjectId}", "/api/gar/children/1405113", (1405113,),
         {"limit": 10}, {"limit": "10"}),
    Case("gar", "get_hierarchy", "GET", "/api/gar/hierarchy/{objectId}", "/api/gar/hierarchy/1405113", (1405113,)),
    Case("gar", "get_stats", "GET", "/api/gar/stats", "/api/gar/stats"),
    Case("gar", "list_regions", "GET", "/api/gar/regions", "/api/gar/regions"),
    Case("gar", "get_region_stats", "GET", "/api/gar/region/{regionCode}/stats", "/api/gar/region/77/stats", ("77",)),
    # Стандартизация адреса
    Case("addressstd", "standardize", "GET", "/api/addressstd", "/api/addressstd", ("москва тверская 1",),
         {"region": 77, "bind": True, "geocode": False},
         {"address": "москва тверская 1", "region": "77", "bind": "true", "geocode": "false"}),
    # Телефон, почта
    Case("phone", "validate", "GET", "/api/phone/{number}", "/api/phone/+79161234567", ("+79161234567",),
         {"country_code": "RU"}, {"countryCode": "RU"}),
    Case("email", "validate", "GET", "/api/emailvalidation", "/api/emailvalidation", ("test@example.com",), {},
         {"email": "test@example.com"}),
    # OCR
    Case("ocr", "recognize", "POST", "/api/ocr/image-to-text", "/api/ocr/image-to-text", (b"\x89PNG",),
         {"mode": "auto"}, body={"image": b64(b"\x89PNG"), "mode": "auto"}),
    # DNS
    Case("dns", "lookup", "GET", "/api/dns/lookup", "/api/dns/lookup", ("atlorium.com",), {"resolver": "1.1.1.1"},
         {"domain": "atlorium.com", "resolver": "1.1.1.1"}),
    Case("dns", "check_propagation", "GET", "/api/dns/propagation", "/api/dns/propagation", ("atlorium.com",),
         {"resolvers": ["1.1.1.1", "8.8.8.8"]}, {"domain": "atlorium.com", "resolvers": "1.1.1.1,8.8.8.8"}),
    # CIDR
    Case("cidr", "calculate", "GET", "/api/cidr/calculate", "/api/cidr/calculate", ("192.168.1.10", 24), {},
         {"ip": "192.168.1.10", "mask": "24"}),
    Case("cidr", "split", "GET", "/api/cidr/subnets", "/api/cidr/subnets", ("10.0.0.0/24", 26), {},
         {"cidr": "10.0.0.0/24", "newMask": "26"}),
    Case("cidr", "check", "GET", "/api/cidr/check", "/api/cidr/check", ("10.0.0.0/8", "10.1.2.3"), {},
         {"cidr": "10.0.0.0/8", "ip": "10.1.2.3"}),
    Case("cidr", "supernet", "POST", "/api/cidr/supernet", "/api/cidr/supernet", (["10.0.0.0/24", "10.0.1.0/24"],),
         body={"inputs": ["10.0.0.0/24", "10.0.1.0/24"]}),
    # Cron
    Case("cron", "evaluate", "POST", "/api/cron/evaluate", "/api/cron/evaluate", ("*/15 * * * *",),
         {"time_zone_id": "Europe/Moscow", "take": 3},
         body={"expression": "*/15 * * * *", "timeZoneId": "Europe/Moscow", "take": 3}),
    Case("cron", "build", "POST", "/api/cron/build", "/api/cron/build", (),
         {"template": CronTemplateType.WEEKLY, "time_of_day": "09:30:00",
          "week_days": [DayOfWeek.MONDAY, DayOfWeek.FRIDAY]},
         body={"template": 5, "timeOfDay": "09:30:00", "weekDays": [1, 5]}),
    # SSL
    Case("certificate", "check", "GET", "/api/certificate", "/api/certificate", ("atlorium.com",), {"port": 443},
         {"host": "atlorium.com", "port": "443"}),
    Case("certificate", "check_url", "GET", "/api/certificate/url", "/api/certificate/url", ("https://atlorium.com",),
         {}, {"url": "https://atlorium.com"}),
    Case("certificate", "check_batch", "GET", "/api/certificate/batch", "/api/certificate/batch",
         (["a.ru", "b.ru"],), {}, {"hosts": "a.ru,b.ru"}),
    # Погода
    Case("weather", "get", "GET", "/api/weather", "/api/weather", (55.75, 37.62), {},
         {"latitude": "55.75", "longitude": "37.62"}),
    # ИИ-чат
    Case("aichat", "send", "POST", "/api/aichat/send", "/api/aichat/send", ("Привет",), {"session_id": "abc"},
         body={"message": "Привет", "sessionId": "abc"}),
    Case("aichat", "get_session", "GET", "/api/aichat/session/{sessionId}", "/api/aichat/session/abc", ("abc",)),
    Case("aichat", "delete_session", "DELETE", "/api/aichat/session/{sessionId}", "/api/aichat/session/abc", ("abc",)),
    Case("aichat", "list_models", "GET", "/api/aichat/models", "/api/aichat/models"),
    # Прямой геокодинг
    Case("geocodeforward", "search", "GET", "/api/geocodeforward", "/api/geocodeforward", ("Москва, Тверская 1",),
         {"size": 1, "exact_only": True}, {"text": "Москва, Тверская 1", "size": "1", "exactOnly": "true"}),
    Case("geocodeforward", "search_structured", "GET", "/api/geocodeforward/structured",
         "/api/geocodeforward/structured", (), {"address": "Тверская 1", "locality": "Москва", "postal_code": "125009"},
         {"address": "Тверская 1", "locality": "Москва", "postalCode": "125009"}),
    Case("geocodeforward", "search_batch", "POST", "/api/geocodeforward/batch", "/api/geocodeforward/batch",
         (["Москва", "Казань"],), {"size_per_query": 2}, body={"queries": ["Москва", "Казань"], "sizePerQuery": 2}),
    Case("geocodeforward", "get_place", "GET", "/api/geocodeforward/place", "/api/geocodeforward/place", ("osm:123",),
         {"include_boundary": True}, {"placeId": "osm:123", "includeBoundary": "true"}),
    Case("geocodeforward", "search_postcode", "GET", "/api/geocodeforward/postcode", "/api/geocodeforward/postcode",
         ("125009",), {}, {"code": "125009"}),
    # Обратный геокодинг
    Case("geocodereverse", "lookup", "GET", "/api/geocodereverse", "/api/geocodereverse", (55.75, 37.62),
         {"include_admin": True}, {"lat": "55.75", "lon": "37.62", "includeAdmin": "true"}),
    Case("geocodereverse", "nearby", "GET", "/api/geocodereverse/nearby", "/api/geocodereverse/nearby", (55.75, 37.62),
         {"radius_km": 1.5, "size": 5}, {"lat": "55.75", "lon": "37.62", "radiusKm": "1.5", "size": "5"}),
    # Тестовые данные
    Case("testdata", "generate", "GET", "/api/testdata", "/api/testdata", (),
         {"count": 2, "fields": ["fullName", "innPerson"], "seed": 42},
         {"count": "2", "fields": "fullName,innPerson", "seed": "42"}),
    Case("testdata", "generate_with_body", "POST", "/api/testdata", "/api/testdata", (),
         {"count": 2, "fields": ["fullName"], "gender": "female"},
         body={"count": 2, "fields": ["fullName"], "gender": "female"}),
    Case("testdata", "list_fields", "GET", "/api/testdata/fields", "/api/testdata/fields"),
    # Проверка ссылок
    Case("urlcheck", "check", "GET", "/api/urlcheck", "/api/urlcheck", ("https://example.com",), {},
         {"url": "https://example.com"}),
    Case("urlcheck", "check_batch", "POST", "/api/urlcheck/batch", "/api/urlcheck/batch",
         (["https://a.ru", "https://b.ru"],), body=["https://a.ru", "https://b.ru"]),
    # Аудит сайта
    Case("pagespeed", "audit", "GET", "/api/pagespeed", "/api/pagespeed", ("https://atlorium.com",),
         {"strategy": "mobile", "force_refresh": True},
         {"url": "https://atlorium.com", "strategy": "mobile", "forceRefresh": "true"}),
    Case("pagespeed", "audit_batch", "POST", "/api/pagespeed/batch", "/api/pagespeed/batch", (["https://a.ru"],),
         {"strategy": "desktop"}, {"strategy": "desktop"}, body=["https://a.ru"]),
    # Модерация изображений
    Case("imagecheck", "analyze", "POST", "/api/imagecheck", "/api/imagecheck", (b"img",),
         {"include_web_search": True}, body={"image": b64(b"img"), "includeWebSearch": True}),
]  # fmt: skip


class Recorder:
    """Подменный сервер: запоминает запросы и отвечает заданной функцией."""

    def __init__(self, respond: Callable[[httpx.Request], httpx.Response] | None = None) -> None:
        self.requests: list[httpx.Request] = []
        self._respond = respond or (lambda request: httpx.Response(200, json={"ok": True}))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return self._respond(request)


def sync_client(recorder: Recorder, **kwargs: Any) -> Atlorium:
    http = httpx.Client(transport=httpx.MockTransport(recorder))
    return Atlorium("ak_test", http_client=http, max_retries=0, **kwargs)


def check_request(case: Case, request: httpx.Request) -> None:
    assert request.method == case.http
    assert request.url.path == case.path
    assert dict(request.url.params) == case.query
    assert request.headers["Authorization"] == "Bearer ak_test"
    if case.body is NO_BODY:
        assert request.content == b""
    else:
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == case.body


def spec_routes() -> set[tuple[str, str]]:
    routes: set[tuple[str, str]] = set()
    for spec_file in sorted((ROOT / "spec").glob("*_ru.json")):
        spec = json.loads(spec_file.read_text(encoding="utf-8"))
        for path, methods in spec["paths"].items():
            for method in methods:
                if method in {"get", "post", "put", "delete", "patch"}:
                    routes.add((method.upper(), path.lower()))
    return routes


# ── Покрытие и форма запросов ───────────────────────────────────────────────────


def test_every_spec_operation_has_a_case() -> None:
    assert len(CASES) == 59
    assert {(case.http, case.route.lower()) for case in CASES} == spec_routes()
    assert len({case.id for case in CASES}) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
def test_sync_request_shape(case: Case) -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    getattr(getattr(client, case.resource), case.method)(*case.args, **case.kwargs)
    assert len(recorder.requests) == 1
    check_request(case, recorder.requests[0])


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
async def test_async_request_shape(case: Case) -> None:
    recorder = Recorder()
    async with httpx.AsyncClient(transport=httpx.MockTransport(recorder)) as http:
        client = AsyncAtlorium("ak_test", http_client=http, max_retries=0)
        await getattr(getattr(client, case.resource), case.method)(*case.args, **case.kwargs)
    assert len(recorder.requests) == 1
    check_request(case, recorder.requests[0])


def test_path_segments_are_escaped() -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    client.phone.validate("+7 916 123-45-67")
    client.egrul.get("ООО/Ромашка")
    assert recorder.requests[0].url.raw_path == b"/api/phone/%2B7%20916%20123-45-67"
    assert recorder.requests[1].url.raw_path.startswith(b"/api/egrul/%D0%9E%D0%9E%D0%9E%2F")


def test_single_string_for_list_arguments_is_not_split() -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    client.urlcheck.check_batch("https://a.ru")
    client.certificate.check_batch("a.ru")
    client.cidr.supernet("10.0.0.0/24")
    client.testdata.generate(fields="fullName")
    client.testdata.generate_with_body(fields="fullName")
    assert json.loads(recorder.requests[0].content) == ["https://a.ru"]
    assert recorder.requests[1].url.params["hosts"] == "a.ru"
    assert json.loads(recorder.requests[2].content) == {"inputs": ["10.0.0.0/24"]}
    assert recorder.requests[3].url.params["fields"] == "fullName"
    assert json.loads(recorder.requests[4].content) == {"fields": ["fullName"]}


def test_optional_arguments_are_not_sent() -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    client.geocodereverse.lookup(55.75, 37.62)
    client.aichat.send("Привет")
    assert dict(recorder.requests[0].url.params) == {"lat": "55.75", "lon": "37.62"}
    assert json.loads(recorder.requests[1].content) == {"message": "Привет"}


# ── Ответы ──────────────────────────────────────────────────────────────────────


FIXTURE_TYPES: dict[str, Any] = {
    "egrul": egrul.CompanyLookupResult,
    "testdata": testdata.TestDataResponse,
    "aichat": aichat.AiChatResponse,
    "cron": cron.CronEvaluationResult,
    "dns": dns.DnsLookupResponse,
}


@pytest.mark.parametrize("name", sorted(FIXTURE_TYPES))
def test_live_fixture_fields_are_described_in_types(name: str) -> None:
    """Живые ответы песочницы (15.09.2026) не содержат полей, которых нет в моделях."""
    assert set(load_fixture(name)) <= set(FIXTURE_TYPES[name].__annotations__)


def test_typed_response_from_live_fixture() -> None:
    body = load_fixture("egrul")
    client = sync_client(Recorder(lambda request: httpx.Response(200, json=body)))
    card = client.egrul.get("7707083893")
    assert card["inn"] == "7707083893"
    okved = card["primaryOkved"]
    assert okved is not None
    assert okved["code"] == "62.01"


def test_excerpt_returns_pdf_bytes() -> None:
    pdf = httpx.Response(200, content=b"%PDF-1.7", headers={"Content-Type": "application/pdf"})
    client = sync_client(Recorder(lambda request: pdf))
    assert client.egrul.get_excerpt("7707083893") == b"%PDF-1.7"


def test_testdata_csv_returns_text() -> None:
    csv_text = "fullName;innPerson\nИванов Иван;026881836682\n"

    def respond(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=csv_text.encode(), headers={"Content-Type": "text/csv; charset=utf-8"})

    recorder = Recorder(respond)
    client = sync_client(recorder)
    from_query: str = client.testdata.generate(format="csv", count=1)
    from_body: str = client.testdata.generate_with_body(format="csv")
    assert from_query == csv_text
    assert from_body == csv_text
    assert recorder.requests[0].url.params["format"] == "csv"
    assert json.loads(recorder.requests[1].content) == {"format": "csv"}


def test_testdata_json_and_seed_header() -> None:
    body = load_fixture("testdata")
    headers = {"X-Atlorium-Seed": "42"}
    client = sync_client(Recorder(lambda request: httpx.Response(200, json=body, headers=headers)))
    result = client.testdata.generate(count=2, seed=42)
    assert result["records"][0]["fullName"]
    raw = client.testdata.with_raw_response.generate(count=2, seed=42)
    assert raw.headers["X-Atlorium-Seed"] == "42"
    assert isinstance(raw.data, dict)


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        ('"Сессия удалена."'.encode(), "application/json; charset=utf-8"),
        ("Сессия удалена.".encode(), "text/plain; charset=utf-8"),
    ],
)
def test_delete_session_returns_string(content: bytes, content_type: str) -> None:
    response = httpx.Response(200, content=content, headers={"Content-Type": content_type})
    client = sync_client(Recorder(lambda request: response))
    assert client.aichat.delete_session("abc") == "Сессия удалена."


def test_raw_response_on_resource() -> None:
    headers = {"X-Atlorium-Sandbox": "true"}
    client = sync_client(Recorder(lambda request: httpx.Response(200, json={"found": True}, headers=headers)))
    raw = client.egrul.with_raw_response.get("7707083893")
    assert isinstance(raw, atlorium.ApiResponse)
    assert raw.status_code == 200
    assert raw.is_sandbox
    assert raw.data["found"] is True
    assert raw.request_id is None
    assert raw.rate_limit is None


async def test_async_raw_response_on_resource() -> None:
    headers = {"X-Atlorium-Sandbox": "true"}
    transport = httpx.MockTransport(Recorder(lambda request: httpx.Response(200, json=[], headers=headers)))
    async with httpx.AsyncClient(transport=transport) as http:
        client = AsyncAtlorium("ak_test", http_client=http)
        raw = await client.gar.with_raw_response.list_regions()
    assert raw.is_sandbox
    assert raw.data == []


def test_resource_errors_are_typed() -> None:
    body = {"error": "not_found", "title": "Ничего не найдено", "message": "Организация не найдена в реестре"}
    client = sync_client(Recorder(lambda request: httpx.Response(404, json=body)))
    with pytest.raises(atlorium.NotFoundError, match="не найдена") as info:
        client.egrul.get("0000000000")
    assert info.value.error_code == "not_found"


# ── Таймауты, изображения, жизненный цикл ───────────────────────────────────────


@pytest.mark.parametrize(
    ("resource", "method", "args", "expected"),
    [
        ("egrul", "get", ("7707083893",), 30.0),
        ("ocr", "recognize", (b"x",), 120.0),
        ("pagespeed", "audit", ("https://a.ru",), 120.0),
        ("pagespeed", "audit_batch", (["https://a.ru"],), 600.0),
        ("aichat", "send", ("Привет",), 660.0),
        ("imagecheck", "analyze", (b"x",), 60.0),
    ],
)
def test_operation_default_timeouts(resource: str, method: str, args: tuple[Any, ...], expected: float) -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    getattr(getattr(client, resource), method)(*args)
    assert recorder.requests[0].extensions["timeout"]["read"] == expected


def test_timeout_overrides() -> None:
    recorder = Recorder()
    client = sync_client(recorder, timeout=900)
    client.ocr.recognize(b"x")
    client.ocr.recognize(b"x", timeout=5)
    assert [request.extensions["timeout"]["read"] for request in recorder.requests] == [900, 5]


def test_image_inputs() -> None:
    expected = b64(PNG.read_bytes())
    assert encode_image(PNG) == expected
    assert encode_image(str(PNG)) == expected
    assert encode_image(PNG.read_bytes()) == expected
    with PNG.open("rb") as stream:
        assert encode_image(stream) == expected
    assert encode_image(expected) == expected
    assert encode_image("data:image/png;base64,AAAA") == "data:image/png;base64,AAAA"
    assert encode_image("iVBORw0KGgo/AAAA+BBBB==") == "iVBORw0KGgo/AAAA+BBBB=="
    for missing in ("scan.png", "./docs/scan.v2", r"C:\docs\scan", "photo.JPG"):
        with pytest.raises(FileNotFoundError, match="не найден"):
            encode_image(missing)
    with pytest.raises(ValueError, match="ссылку"):
        encode_image("https://example.com/a.png")
    with PNG.open(encoding="latin-1") as text_stream, pytest.raises(TypeError, match="бинарном"):
        encode_image(text_stream)  # type: ignore[arg-type]


def test_ocr_and_imagecheck_send_file_from_path() -> None:
    recorder = Recorder()
    client = sync_client(recorder)
    client.ocr.recognize(PNG)
    client.imagecheck.analyze(str(PNG), include_text=False)
    expected = b64(PNG.read_bytes())
    assert json.loads(recorder.requests[0].content) == {"image": expected}
    assert json.loads(recorder.requests[1].content) == {"image": expected, "includeText": False}


def test_resources_are_cached_and_bound_to_client() -> None:
    client = sync_client(Recorder())
    assert client.egrul is client.egrul
    assert client.egrul.with_raw_response is client.egrul.with_raw_response
    copy = client.with_options(timeout=5)
    assert copy.egrul is not client.egrul
    assert copy.egrul._client is copy
