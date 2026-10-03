"""
Ответ с метаданными: статус, заголовки, признак песочницы, остатки лимита.

Обычные методы возвращают сразу данные. Чтобы получить ещё и метаданные, вызовите тот же
метод через ``with_raw_response``:

    raw = client.egrul.with_raw_response.get("7707083893")
    print(raw.status_code, raw.is_sandbox, raw.rate_limit)
    card = raw.data
"""

from __future__ import annotations

import contextvars
import email.utils
import functools
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar, cast

import httpx

__all__ = ["ApiResponse", "RateLimitInfo"]

T = TypeVar("T")
P = ParamSpec("P")

SANDBOX_HEADER = "X-Atlorium-Sandbox"

# Флаг «вернуть ApiResponse вместо данных». Контекстная переменная, а не аргумент метода:
# так сигнатуры ресурсов остаются чистыми, а флаг корректно живёт и в потоках, и в asyncio.
_RAW_RESPONSE: contextvars.ContextVar[bool] = contextvars.ContextVar("atlorium_raw_response", default=False)


@dataclass(frozen=True)
class RateLimitInfo:
    """Остатки лимита из заголовков ``X-RateLimit-*`` / ``RateLimit-*``, если сервер их прислал."""

    limit: int | None = None
    remaining: int | None = None
    reset: float | None = None


@dataclass(frozen=True)
class ApiResponse(Generic[T]):
    """Данные ответа вместе с HTTP-метаданными."""

    data: T
    """Разобранное тело ответа — то же, что возвращает обычный вызов метода."""

    http_response: httpx.Response
    """Исходный ответ ``httpx`` — для всего, что не вынесено в свойства."""

    @property
    def status_code(self) -> int:
        """HTTP-статус ответа."""
        return self.http_response.status_code

    @property
    def headers(self) -> httpx.Headers:
        """Заголовки ответа (регистронезависимый словарь)."""
        return self.http_response.headers

    @property
    def is_sandbox(self) -> bool:
        """``True``, если сервер пометил ответ заголовком ``X-Atlorium-Sandbox: true``.

        Внимание: у полностью локальных сервисов (например, генератора тестовых данных)
        заголовка нет даже на демо-ключе — ответ там настоящий.
        """
        return str(self.headers.get(SANDBOX_HEADER, "")).strip().lower() == "true"

    @property
    def request_id(self) -> str | None:
        """Идентификатор запроса из ``X-Request-Id``, если сервер его прислал."""
        value = self.headers.get("X-Request-Id") or self.headers.get("Request-Id")
        return str(value) if value else None

    @property
    def rate_limit(self) -> RateLimitInfo | None:
        """Остатки лимита или ``None``, если сервер не отдаёт соответствующие заголовки."""
        return parse_rate_limit(self.headers)

    @property
    def retry_after(self) -> float | None:
        """Значение ``Retry-After`` в секундах, если заголовок есть."""
        return parse_retry_after(self.headers)


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(float(value.strip()))
    except ValueError:
        return None


def parse_rate_limit(headers: httpx.Headers) -> RateLimitInfo | None:
    """Разбирает заголовки остатков лимита (оба распространённых варианта именования)."""
    for prefix in ("X-RateLimit-", "RateLimit-"):
        limit = _to_int(headers.get(prefix + "Limit"))
        remaining = _to_int(headers.get(prefix + "Remaining"))
        reset_raw = headers.get(prefix + "Reset")
        reset = float(reset_raw) if reset_raw and reset_raw.strip().replace(".", "", 1).isdigit() else None
        if limit is not None or remaining is not None or reset is not None:
            return RateLimitInfo(limit=limit, remaining=remaining, reset=reset)
    return None


def parse_retry_after(headers: httpx.Headers) -> float | None:
    """Разбирает ``Retry-After``: число секунд или HTTP-дата (RFC 9110 §10.2.3)."""
    raw = headers.get("Retry-After")
    if not raw:
        return None
    raw = raw.strip()
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        moment = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    return max(0.0, moment.timestamp() - time.time())


def is_raw_response_mode() -> bool:
    """Включён ли сейчас режим ``with_raw_response``."""
    return _RAW_RESPONSE.get()


def to_raw_response_wrapper(func: Callable[P, T]) -> Callable[P, ApiResponse[T]]:
    """Оборачивает синхронный метод ресурса так, чтобы он возвращал :class:`ApiResponse`."""

    @functools.wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> ApiResponse[T]:
        token = _RAW_RESPONSE.set(True)
        try:
            return cast("ApiResponse[T]", func(*args, **kwargs))
        finally:
            _RAW_RESPONSE.reset(token)

    return wrapped


def to_async_raw_response_wrapper(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[ApiResponse[T]]]:
    """Оборачивает асинхронный метод ресурса так, чтобы он возвращал :class:`ApiResponse`."""

    @functools.wraps(func)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> ApiResponse[T]:
        token = _RAW_RESPONSE.set(True)
        try:
            return cast("ApiResponse[T]", await func(*args, **kwargs))
        finally:
            _RAW_RESPONSE.reset(token)

    return wrapped
