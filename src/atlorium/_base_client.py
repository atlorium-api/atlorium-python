"""
Транспортное ядро: заголовки, сериализация параметров, ретраи, разбор ответов и ошибок.

Синхронный :class:`SyncAPIClient` и асинхронный :class:`AsyncAPIClient` делят всю логику,
кроме самого отправления запроса и паузы между попытками.
"""

from __future__ import annotations

import asyncio
import enum
import json as jsonlib
import os
import platform
import random
import time
import warnings
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Literal

import httpx

from ._exceptions import (
    PLANNED_UNAVAILABILITY_CODES,
    APIConnectionError,
    APITimeoutError,
    AtloriumError,
    error_code_of,
    make_status_error,
)
from ._response import ApiResponse, is_raw_response_mode, parse_retry_after
from ._version import __version__

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "MAX_RETRY_DELAY",
    "SANDBOX_API_KEY",
    "AsyncAPIClient",
    "AtloriumSandboxWarning",
    "RequestOptions",
    "SyncAPIClient",
]

SANDBOX_API_KEY = "ak_sandbox_demo_mockdata_v1"
"""Публичный демо-ключ. С ним API отвечает детерминированными моками, а не реальными данными."""

DEFAULT_BASE_URL = "https://atlorium.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2

MAX_RETRY_DELAY = 120.0
"""Потолок ожидания перед повтором, секунд. Сервер может попросить подождать десятки минут
(исчерпан лимит запросов или сайт на обслуживании) — ждать столько внутри вызова нельзя,
поэтому такой ответ сразу превращается в исключение своего статуса с ``retry_after``."""

INITIAL_RETRY_DELAY = 0.5
MAX_BACKOFF_DELAY = 8.0

RETRYABLE_STATUSES = frozenset({429, 503})
"""Статусы, которые повторяются. Исключение — 503 с кодом плановых работ (см. ``_retry_delay_for_response``)."""

# Сетевые ошибки, при которых запрос точно не дошёл до сервера: соединение не установилось.
# Только их безопасно повторять для POST — POST-операции платные и неидемпотентные, и повтор
# после таймаута чтения или обрыва мог бы выполнить операцию (и списать деньги) второй раз.
_NOT_SENT_ERRORS: tuple[type[httpx.TransportError], ...] = (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout)

ResponseType = Literal["json", "bytes", "text", "auto"]


@dataclass(frozen=True)
class RequestOptions:
    """Описание одного вызова API — то, что ресурс передаёт транспорту."""

    method: str
    path: str
    params: Mapping[str, Any] | None = None
    json: Any = None
    has_body: bool = False
    timeout: float | None = None
    """Таймаут этого вызова, заданный пользователем. Имеет наивысший приоритет."""
    default_timeout: float | None = None
    """Минимальный таймаут операции по умолчанию (например, 660 с у ИИ-чата)."""
    response_type: ResponseType = "json"


def serialize_query_value(value: Any) -> str:
    """Приводит значение параметра строки запроса к виду, который понимает сервер."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, enum.Enum):
        return serialize_query_value(value.value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return ",".join(serialize_query_value(item) for item in value)
    return str(value)


QueryItems = list[tuple[str, "str | int | float | bool | None"]]


def build_query(params: Mapping[str, Any] | None) -> QueryItems:
    """Отбрасывает непереданные (``None``) параметры — тогда действует серверный дефолт."""
    if not params:
        return []
    return [(key, serialize_query_value(value)) for key, value in params.items() if value is not None]


def _user_agent() -> str:
    return f"atlorium-python/{__version__} ({platform.python_implementation()}/{platform.python_version()})"


class AtloriumSandboxWarning(UserWarning):
    """Клиент создан без API-ключа и работает на публичном демо-ключе: ответы — моки."""


class BaseClient:
    """Общая часть синхронного и асинхронного клиентов."""

    base_url: str
    timeout: float
    max_retries: int

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        timeout: float | None,
        max_retries: int | None,
    ) -> None:
        resolved_key = (api_key or "").strip() or os.environ.get("ATLORIUM_API_KEY", "").strip()
        if not resolved_key:
            # Молча перейти на моки в проде опасно: проверки контрагентов вернут выдуманные данные.
            warnings.warn(
                "API-ключ Atlorium не задан (ни аргументом api_key, ни переменной ATLORIUM_API_KEY) — "
                "клиент работает на публичном демо-ключе, ответы API — моки, а не реальные данные. "
                "Чтобы явно выбрать демо-режим без предупреждения, передайте api_key=atlorium.SANDBOX_API_KEY.",
                AtloriumSandboxWarning,
                stacklevel=4,
            )
            resolved_key = SANDBOX_API_KEY
        # Ключ храним в «приватном» атрибуте и не показываем ни в repr, ни в исключениях.
        self._api_key = resolved_key
        self.base_url = (base_url or os.environ.get("ATLORIUM_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = DEFAULT_TIMEOUT if timeout is None else float(timeout)
        self.max_retries = DEFAULT_MAX_RETRIES if max_retries is None else int(max_retries)
        if self.max_retries < 0:
            raise ValueError("max_retries не может быть отрицательным")

    @property
    def is_sandbox(self) -> bool:
        """``True``, если клиент работает на публичном демо-ключе (ответы — моки)."""
        return self._api_key == SANDBOX_API_KEY

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self.base_url!r}, is_sandbox={self.is_sandbox})"

    # ── Построение запроса ──────────────────────────────────────────────────────

    @property
    def default_headers(self) -> dict[str, str]:
        """Заголовки, которые уходят с каждым запросом."""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": _user_agent(),
        }

    def _effective_timeout(self, options: RequestOptions) -> float:
        if options.timeout is not None:
            return float(options.timeout)
        if options.default_timeout is not None:
            return max(self.timeout, options.default_timeout)
        return self.timeout

    def _build_request(self, http: httpx.Client | httpx.AsyncClient, options: RequestOptions) -> httpx.Request:
        headers = self.default_headers
        content: bytes | None = None
        if options.has_body:
            headers["Content-Type"] = "application/json"
            content = jsonlib.dumps(options.json, ensure_ascii=False, default=_json_default).encode("utf-8")
        return http.build_request(
            options.method,
            self.base_url + options.path,
            params=build_query(options.params),
            headers=headers,
            content=content,
            timeout=self._effective_timeout(options),
        )

    # ── Ретраи ──────────────────────────────────────────────────────────────────

    @staticmethod
    def _retry_after_from(response: httpx.Response) -> float | None:
        header_value = parse_retry_after(response.headers)
        if header_value is not None:
            return header_value
        body = _safe_json(response)
        if isinstance(body, dict):
            value = body.get("retryAfterSeconds")
            if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                return float(value)
        return None

    @staticmethod
    def _can_retry_transport_error(options: RequestOptions, error: httpx.TransportError) -> bool:
        """GET и DELETE повторяются при любой сетевой ошибке, POST — только если запрос не ушёл."""
        return options.method.upper() != "POST" or isinstance(error, _NOT_SENT_ERRORS)

    @staticmethod
    def _backoff_delay(attempt: int) -> float:
        """Экспоненциальная задержка с джиттером: 0.5, 1, 2, 4, 8 с (±25 %)."""
        base: float = min(INITIAL_RETRY_DELAY * (2**attempt), MAX_BACKOFF_DELAY)
        return base * (0.75 + random.random() * 0.5)  # noqa: S311 — джиттер, не криптография

    def _retry_delay_for_response(self, response: httpx.Response, attempt: int) -> float | None:
        """Сколько ждать перед повтором или ``None``, если повторять не нужно."""
        if response.status_code not in RETRYABLE_STATUSES or attempt >= self.max_retries:
            return None
        if response.status_code == 503 and error_code_of(_safe_json(response)) in PLANNED_UNAVAILABILITY_CODES:
            # Сервис выключен или идут плановые работы: повтор через секунды ничего не даст.
            return None
        retry_after = self._retry_after_from(response)
        if retry_after is not None:
            # Сервер просит ждать дольше разумного — не вешаем вызов, отдаём ошибку сразу.
            return None if retry_after > MAX_RETRY_DELAY else retry_after
        return self._backoff_delay(attempt)

    # ── Разбор ответа ───────────────────────────────────────────────────────────

    def _process_response(self, response: httpx.Response, options: RequestOptions) -> Any:
        if response.is_success:
            data = _parse_body(response, options.response_type)
            if is_raw_response_mode():
                return ApiResponse(data=data, http_response=response)
            return data

        body = _safe_json(response)
        if body is None:
            body = response.text
        raise make_status_error(
            response.status_code,
            body=body,
            headers=response.headers,
            request_id=response.headers.get("X-Request-Id") or response.headers.get("Request-Id"),
            retry_after=self._retry_after_from(response),
        )

    @staticmethod
    def _transport_error(error: httpx.TransportError) -> AtloriumError:
        if isinstance(error, httpx.TimeoutException):
            return APITimeoutError()
        return APIConnectionError(f"Не удалось подключиться к API Atlorium: {type(error).__name__}")


def _json_default(value: Any) -> Any:
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Значение типа {type(value).__name__} нельзя сериализовать в JSON")


def _is_json_content_type(response: httpx.Response) -> bool:
    content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
    return content_type in ("application/json", "text/json") or content_type.endswith("+json")


def _safe_json(response: httpx.Response) -> Any:
    try:
        response.read()
        if not response.content:
            return None
        return response.json()
    except (ValueError, httpx.ResponseNotRead):
        return None


def _parse_body(response: httpx.Response, response_type: ResponseType) -> Any:
    if response_type == "bytes":
        return response.content
    if response_type == "text":
        return response.text
    if not response.content:
        return None
    if response_type == "auto" and not _is_json_content_type(response):
        # Сервер вернул не JSON (например, CSV или простой текст) — отдаём как строку.
        try:
            return response.json()
        except ValueError:
            return response.text
    return response.json()


class SyncAPIClient(BaseClient):
    """Синхронный транспорт поверх ``httpx.Client``."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        timeout: float | None,
        max_retries: int | None,
        http_client: httpx.Client | None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._owns_http_client = http_client is None
        self._http = http_client if http_client is not None else httpx.Client(follow_redirects=True)
        self._sleep: Callable[[float], None] = time.sleep

    def request(self, options: RequestOptions) -> Any:
        """Выполняет вызов с ретраями на 429, 503 (кроме плановых работ) и сетевые ошибки."""
        attempt = 0
        while True:
            request = self._build_request(self._http, options)
            try:
                response = self._http.send(request)
            except httpx.TransportError as error:
                if attempt < self.max_retries and self._can_retry_transport_error(options, error):
                    self._sleep(self._backoff_delay(attempt))
                    attempt += 1
                    continue
                raise self._transport_error(error) from error

            delay = self._retry_delay_for_response(response, attempt)
            if delay is not None:
                response.close()
                self._sleep(delay)
                attempt += 1
                continue
            return self._process_response(response, options)

    def close(self) -> None:
        """Закрывает HTTP-соединения, если клиент создавал их сам."""
        if self._owns_http_client:
            self._http.close()


class AsyncAPIClient(BaseClient):
    """Асинхронный транспорт поверх ``httpx.AsyncClient``."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        timeout: float | None,
        max_retries: int | None,
        http_client: httpx.AsyncClient | None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._owns_http_client = http_client is None
        self._http = http_client if http_client is not None else httpx.AsyncClient(follow_redirects=True)
        self._sleep: Callable[[float], Awaitable[None]] = asyncio.sleep

    async def request(self, options: RequestOptions) -> Any:
        """Выполняет вызов с ретраями на 429, 503 (кроме плановых работ) и сетевые ошибки."""
        attempt = 0
        while True:
            request = self._build_request(self._http, options)
            try:
                response = await self._http.send(request)
            except httpx.TransportError as error:
                if attempt < self.max_retries and self._can_retry_transport_error(options, error):
                    await self._sleep(self._backoff_delay(attempt))
                    attempt += 1
                    continue
                raise self._transport_error(error) from error

            delay = self._retry_delay_for_response(response, attempt)
            if delay is not None:
                await response.aclose()
                await self._sleep(delay)
                attempt += 1
                continue
            await response.aread()
            return self._process_response(response, options)

    async def close(self) -> None:
        """Закрывает HTTP-соединения, если клиент создавал их сам."""
        if self._owns_http_client:
            await self._http.aclose()


def path_segment(value: Any) -> str:
    """Экранирует значение для подстановки в путь (``/``, пробелы, кириллица)."""
    from urllib.parse import quote

    return quote(serialize_query_value(value), safe="")


def ensure_sequence(value: str | Sequence[str]) -> list[str]:
    """Принимает строку или последовательность строк, возвращает список."""
    if isinstance(value, str):
        return [value]
    return list(value)
