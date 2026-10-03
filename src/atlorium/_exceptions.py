"""
Иерархия исключений SDK.

Все ошибки наследуются от :class:`AtloriumError`, поэтому достаточно одного ``except``:

    try:
        card = client.egrul.get("7707083893")
    except atlorium.NotFoundError:
        ...  # организации нет в реестре
    except atlorium.AtloriumError as error:
        print(error.status, error.message)

Сетевые ошибки названы ``APIConnectionError`` / ``APITimeoutError``, чтобы не затенять
встроенные ``ConnectionError`` / ``TimeoutError``.
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = [
    "APIConnectionError",
    "APITimeoutError",
    "AtloriumError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "ServiceUnavailableError",
    "ValidationError",
]

PLANNED_UNAVAILABILITY_CODES = frozenset({"service_disabled", "maintenance"})
"""Коды 503 «плановые работы / сервис выключен»: повтор через секунды бесполезен, SDK их не повторяет."""

_SERVICE_NOT_IN_TERMS = (
    "Сервис не входит в условия вашей учётной записи. Чтобы подключить его, напишите на support@atlorium.com"
)

# Человекочитаемые причины по коду HTTP — те же формулировки, что в примерах Atlorium на других языках.
_REASONS: dict[int, str] = {
    400: "Неверный формат входных данных",
    401: "API-ключ отсутствует, просрочен или недействителен",
    402: "Недостаточно кредитов на балансе — пополните на https://atlorium.com",
    403: _SERVICE_NOT_IN_TERMS,
    404: "Объект не найден либо маршрут не существует",
    429: "Превышен лимит запросов — повторите позже",
    503: (
        "Сервис временно недоступен: сбой внешнего источника данных или плановые работы "
        "(состояние — https://atlorium.com/status). Деньги за такой ответ не списываются"
    ),
}


class AtloriumError(Exception):
    """Базовая ошибка SDK.

    Атрибуты:
        status: HTTP-статус ответа; ``None`` для сетевых ошибок.
        message: человекочитаемое сообщение на русском.
        body: тело ответа — разобранный JSON (обычно объект ``ApiError``) или текст.
        headers: заголовки ответа (``None`` для сетевых ошибок).
        request_id: идентификатор запроса из заголовка ``X-Request-Id``, если сервер его прислал.
        error_code: машинный код ошибки из тела (``bad_request``, ``rate_limited_client``,
            ``rate_limited_global``, ``service_disabled`` и т.п.).
        retry_after: через сколько секунд сервер разрешает повторить запрос — из заголовка
            ``Retry-After`` или поля ``retryAfterSeconds`` тела; ``None``, если сервер не сообщил.
    """

    status: int | None
    message: str
    body: Any
    headers: httpx.Headers | None
    request_id: str | None
    error_code: str | None
    retry_after: float | None

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        body: Any = None,
        headers: httpx.Headers | None = None,
        request_id: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.body = body
        self.headers = headers
        self.request_id = request_id
        self.error_code = error_code_of(body)
        self.retry_after = retry_after

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status={self.status!r}, message={self.message!r})"


class APIConnectionError(AtloriumError):
    """Не удалось связаться с сервером: DNS, обрыв соединения, TLS и т.п."""

    def __init__(self, message: str = "Не удалось подключиться к API Atlorium") -> None:
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """Сервер не ответил за отведённое время (параметр ``timeout``)."""

    def __init__(self, message: str = "Истекло время ожидания ответа API Atlorium") -> None:
        super().__init__(message)


class ValidationError(AtloriumError):
    """HTTP 400: неверный формат входных данных. Отклонённый запрос не тарифицируется."""


class AuthenticationError(AtloriumError):
    """HTTP 401: API-ключ отсутствует, просрочен или недействителен."""


class InsufficientCreditsError(AtloriumError):
    """HTTP 402: недостаточно кредитов на балансе.

    Атрибут ``balance`` — текущий баланс, если сервер его сообщил.
    """

    @property
    def balance(self) -> float | None:
        value = self.body.get("balance") if isinstance(self.body, dict) else None
        return float(value) if isinstance(value, (int, float)) else None


class PermissionDeniedError(AtloriumError):
    """HTTP 403: доступ запрещён.

    Код ``service_not_in_account_terms`` — сервис не входит в согласованные условия вашей
    учётной записи. Чтобы подключить его, напишите на support@atlorium.com. Не повторяется.
    """


class NotFoundError(AtloriumError):
    """HTTP 404: объект не найден либо маршрут не существует."""


class RateLimitError(AtloriumError):
    """HTTP 429: превышен лимит запросов.

    Атрибут ``retry_after`` — через сколько секунд сервер разрешает повторить запрос
    (из заголовка ``Retry-After`` или поля ``retryAfterSeconds`` тела), либо ``None``.
    """


class ServerError(AtloriumError):
    """Ответы 5xx: ошибка на стороне сервера. ``except ServerError`` ловит и :class:`ServiceUnavailableError`."""


class ServiceUnavailableError(ServerError):
    """HTTP 503: сервис временно недоступен.

    Сбой внешнего источника данных или плановые работы (коды ``service_disabled``,
    ``maintenance``; состояние — https://atlorium.com/status). Деньги за такой ответ не
    списываются. При плановых работах SDK запрос не повторяет; при прочих 503 повторяет
    автоматически. ``retry_after`` — пауза из заголовка ``Retry-After``, если сервер её сообщил.
    """


def error_code_of(body: Any) -> str | None:
    """Машинный код ошибки — поле ``error`` объекта ``ApiError``."""
    if isinstance(body, dict):
        value = body.get("error")
        if isinstance(value, str):
            return value
    return None


def reason_for(status: int, error_code: str | None = None) -> str:
    """Возвращает человекочитаемую причину для HTTP-кода (и машинного кода ошибки, если он важен)."""
    if status == 403 and error_code not in (None, "service_not_in_account_terms"):
        return "Доступ запрещён"
    if status in _REASONS:
        return _REASONS[status]
    if status >= 500:
        return "Внутренняя ошибка сервера"
    return "Неожиданный ответ сервера"


def extract_server_message(body: Any) -> str | None:
    """Достаёт текст ошибки из тела ответа: поле ``message`` объекта ``ApiError`` или строку."""
    if isinstance(body, dict):
        for key in ("message", "detail", "title"):
            value = body.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None
    if isinstance(body, str) and body.strip():
        return body.strip()[:300]
    return None


def make_status_error(
    status: int,
    *,
    body: Any,
    headers: httpx.Headers,
    request_id: str | None,
    retry_after: float | None,
) -> AtloriumError:
    """Создаёт исключение нужного класса по HTTP-статусу."""
    reason = reason_for(status, error_code_of(body))
    server_message = extract_server_message(body)
    message = f"HTTP {status}: {reason}"
    if server_message:
        message = f"{message}. Ответ сервера: {server_message}"

    error_class: type[AtloriumError]
    if status == 429:
        error_class = RateLimitError
    elif status == 400:
        error_class = ValidationError
    elif status == 401:
        error_class = AuthenticationError
    elif status == 402:
        error_class = InsufficientCreditsError
    elif status == 403:
        error_class = PermissionDeniedError
    elif status == 404:
        error_class = NotFoundError
    elif status == 503:
        error_class = ServiceUnavailableError
    elif status >= 500:
        error_class = ServerError
    else:
        error_class = AtloriumError
    return error_class(
        message, status=status, body=body, headers=headers, request_id=request_id, retry_after=retry_after
    )
