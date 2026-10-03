"""
Ресурс «API проверки почты»: ``client.email``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import email as _types

__all__ = ["AsyncEmailResource", "EmailResource"]


def _validate_options(*, email: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/emailvalidation", params={"email": email}, timeout=timeout)


class EmailResource(SyncAPIResource):
    """
    API проверки почты.

    Примеры на шести языках: https://github.com/atlorium-api/email-verification-api-client
    """

    @cached_property
    def with_raw_response(self) -> EmailResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return EmailResourceWithRawResponse(self)

    def validate(self, email: str, *, timeout: float | None = None) -> _types.EmailValidationReport:
        """
        Проверяет почтовый адрес: существует ли ящик, принимает ли домен почту, не одноразовый
        ли это ящик, не спам-ловушка и не ролевой ли адрес.

        Пример запроса:
        GET /api/emailvalidation?email=user@example.com

        ТАРИФИКАЦИЯ. Запрос не тарифицируется, если адрес синтаксически некорректен (400) либо
        если проверить адрес не удалось и вернулся статус unknown (почтовый сервер домена
        применил greylisting, не ответил или заблокировал проверку). Платите только за
        содержательный вердикт.

        Аргументы:
            email: Почтовый адрес для проверки. Пример: user@example.com
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.EmailValidationReport", self._client.request(_validate_options(email=email, timeout=timeout))
        )


class AsyncEmailResource(AsyncAPIResource):
    """
    API проверки почты.

    Примеры на шести языках: https://github.com/atlorium-api/email-verification-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncEmailResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncEmailResourceWithRawResponse(self)

    async def validate(self, email: str, *, timeout: float | None = None) -> _types.EmailValidationReport:
        """
        Проверяет почтовый адрес: существует ли ящик, принимает ли домен почту, не одноразовый
        ли это ящик, не спам-ловушка и не ролевой ли адрес.

        Пример запроса:
        GET /api/emailvalidation?email=user@example.com

        ТАРИФИКАЦИЯ. Запрос не тарифицируется, если адрес синтаксически некорректен (400) либо
        если проверить адрес не удалось и вернулся статус unknown (почтовый сервер домена
        применил greylisting, не ответил или заблокировал проверку). Платите только за
        содержательный вердикт.

        Аргументы:
            email: Почтовый адрес для проверки. Пример: user@example.com
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.EmailValidationReport", await self._client.request(_validate_options(email=email, timeout=timeout))
        )


class EmailResourceWithRawResponse:
    """Методы :class:`EmailResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: EmailResource) -> None:
        self.validate = to_raw_response_wrapper(resource.validate)


class AsyncEmailResourceWithRawResponse:
    """Методы :class:`AsyncEmailResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncEmailResource) -> None:
        self.validate = to_async_raw_response_wrapper(resource.validate)
