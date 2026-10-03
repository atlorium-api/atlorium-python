"""
Ресурс «API справочника SWIFT/BIC»: ``client.swift``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import swift as _types

__all__ = ["AsyncSwiftResource", "SwiftResource"]


def _get_options(*, bic: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/swift/{path_segment(bic)}", timeout=timeout)


def _search_options(*, query: str, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/swift/search", params={"query": query, "limit": limit}, timeout=timeout
    )


def _validate_options(*, bic: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/swift/validate/{path_segment(bic)}", timeout=timeout)


def _get_stats_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/swift/stats", timeout=timeout)


class SwiftResource(SyncAPIResource):
    """
    API справочника SWIFT/BIC.

    Примеры на шести языках: https://github.com/atlorium-api/swift-bic-api-client
    """

    @cached_property
    def with_raw_response(self) -> SwiftResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return SwiftResourceWithRawResponse(self)

    def get(self, bic: str, *, timeout: float | None = None) -> _types.SwiftBankInfo:
        """
        Возвращает карточку организации по точному SWIFT/BIC (8 или 11 символов).

        Пример запроса:
        GET /api/swift/DEUTDEFF

        Аргументы:
            bic: SWIFT/BIC-код. 8-значный (головной офис) дополняется до 11 ("XXX"). Пример: DEUTDEFF.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.SwiftBankInfo", self._client.request(_get_options(bic=bic, timeout=timeout)))

    def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.SwiftSearchResponse:
        """
        Ищет организации по наименованию (полнотекстовый поиск).

        Примеры запросов:
        GET /api/swift/search?query=Sberbank
        GET /api/swift/search?query=Deutsche%20Bank&limit=50

        Аргументы:
            query: Строка поиска — часть наименования организации. Пример: Sberbank.
            limit: Максимум результатов (по умолчанию 20, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SwiftSearchResponse",
            self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    def validate(self, bic: str, *, timeout: float | None = None) -> _types.SwiftBicValidationResult:
        """
        Проверяет формат SWIFT/BIC по стандарту ISO-9362 и разбирает его на части, мгновенно.
        Проверяет только формат, а не существование такого кода.

        Пример запроса:
        GET /api/swift/validate/DEUTDEFFXXX

        Аргументы:
            bic: Проверяемый BIC (8 или 11 символов).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SwiftBicValidationResult", self._client.request(_validate_options(bic=bic, timeout=timeout))
        )

    def get_stats(self, *, timeout: float | None = None) -> _types.SwiftStatsResponse:
        """
        Возвращает служебную информацию сервиса: готовность отвечать на запросы.

        Пример запроса:
        GET /api/swift/stats

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.SwiftStatsResponse", self._client.request(_get_stats_options(timeout=timeout)))


class AsyncSwiftResource(AsyncAPIResource):
    """
    API справочника SWIFT/BIC.

    Примеры на шести языках: https://github.com/atlorium-api/swift-bic-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncSwiftResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncSwiftResourceWithRawResponse(self)

    async def get(self, bic: str, *, timeout: float | None = None) -> _types.SwiftBankInfo:
        """
        Возвращает карточку организации по точному SWIFT/BIC (8 или 11 символов).

        Пример запроса:
        GET /api/swift/DEUTDEFF

        Аргументы:
            bic: SWIFT/BIC-код. 8-значный (головной офис) дополняется до 11 ("XXX"). Пример: DEUTDEFF.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.SwiftBankInfo", await self._client.request(_get_options(bic=bic, timeout=timeout)))

    async def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.SwiftSearchResponse:
        """
        Ищет организации по наименованию (полнотекстовый поиск).

        Примеры запросов:
        GET /api/swift/search?query=Sberbank
        GET /api/swift/search?query=Deutsche%20Bank&limit=50

        Аргументы:
            query: Строка поиска — часть наименования организации. Пример: Sberbank.
            limit: Максимум результатов (по умолчанию 20, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SwiftSearchResponse",
            await self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    async def validate(self, bic: str, *, timeout: float | None = None) -> _types.SwiftBicValidationResult:
        """
        Проверяет формат SWIFT/BIC по стандарту ISO-9362 и разбирает его на части, мгновенно.
        Проверяет только формат, а не существование такого кода.

        Пример запроса:
        GET /api/swift/validate/DEUTDEFFXXX

        Аргументы:
            bic: Проверяемый BIC (8 или 11 символов).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SwiftBicValidationResult", await self._client.request(_validate_options(bic=bic, timeout=timeout))
        )

    async def get_stats(self, *, timeout: float | None = None) -> _types.SwiftStatsResponse:
        """
        Возвращает служебную информацию сервиса: готовность отвечать на запросы.

        Пример запроса:
        GET /api/swift/stats

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.SwiftStatsResponse", await self._client.request(_get_stats_options(timeout=timeout)))


class SwiftResourceWithRawResponse:
    """Методы :class:`SwiftResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: SwiftResource) -> None:
        self.get = to_raw_response_wrapper(resource.get)
        self.search = to_raw_response_wrapper(resource.search)
        self.validate = to_raw_response_wrapper(resource.validate)
        self.get_stats = to_raw_response_wrapper(resource.get_stats)


class AsyncSwiftResourceWithRawResponse:
    """Методы :class:`AsyncSwiftResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncSwiftResource) -> None:
        self.get = to_async_raw_response_wrapper(resource.get)
        self.search = to_async_raw_response_wrapper(resource.search)
        self.validate = to_async_raw_response_wrapper(resource.validate)
        self.get_stats = to_async_raw_response_wrapper(resource.get_stats)
