"""
Ресурс «API справочника БИК»: ``client.cbr``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import cbr as _types

__all__ = ["AsyncCbrResource", "CbrResource"]


def _get_options(*, bik: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/cbr/{path_segment(bik)}", timeout=timeout)


def _search_options(*, query: str, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/cbr/search", params={"query": query, "limit": limit}, timeout=timeout
    )


def _get_stats_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/cbr/stats", timeout=timeout)


class CbrResource(SyncAPIResource):
    """
    API справочника БИК.

    Примеры на шести языках: https://github.com/atlorium-api/cbr-bik-api-client
    """

    @cached_property
    def with_raw_response(self) -> CbrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return CbrResourceWithRawResponse(self)

    def get(self, bik: str, *, timeout: float | None = None) -> _types.CbrBankInfo:
        """
        Возвращает реквизиты участника справочника по точному БИК (9 цифр).

        Пример запроса:
        GET /api/cbr/044525225

        Аргументы:
            bik: БИК — банковский идентификационный код (ровно 9 цифр). Пример: 044525225 (ПАО Сбербанк).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CbrBankInfo", self._client.request(_get_options(bik=bik, timeout=timeout)))

    def search(self, query: str, *, limit: int | None = None, timeout: float | None = None) -> _types.CbrSearchResponse:
        """
        Ищет участников по наименованию, городу, SWIFT или началу БИК.

        Примеры запросов:
        GET /api/cbr/search?query=Сбербанк
        GET /api/cbr/search?query=0445&limit=50

        Аргументы:
            query: Строка поиска. Если состоит только из цифр — трактуется как БИК (поиск по началу кода), иначе ищется как подстрока в наименовании, населённом пункте и SWIFT.
            limit: Максимальное количество результатов (по умолчанию 20, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CbrSearchResponse", self._client.request(_search_options(query=query, limit=limit, timeout=timeout))
        )

    def get_stats(self, *, timeout: float | None = None) -> _types.CbrStatsResponse:
        """
        Возвращает статистику загруженного справочника: размер, дата актуальности, готовность.

        Пример запроса:
        GET /api/cbr/stats

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CbrStatsResponse", self._client.request(_get_stats_options(timeout=timeout)))


class AsyncCbrResource(AsyncAPIResource):
    """
    API справочника БИК.

    Примеры на шести языках: https://github.com/atlorium-api/cbr-bik-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncCbrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncCbrResourceWithRawResponse(self)

    async def get(self, bik: str, *, timeout: float | None = None) -> _types.CbrBankInfo:
        """
        Возвращает реквизиты участника справочника по точному БИК (9 цифр).

        Пример запроса:
        GET /api/cbr/044525225

        Аргументы:
            bik: БИК — банковский идентификационный код (ровно 9 цифр). Пример: 044525225 (ПАО Сбербанк).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CbrBankInfo", await self._client.request(_get_options(bik=bik, timeout=timeout)))

    async def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.CbrSearchResponse:
        """
        Ищет участников по наименованию, городу, SWIFT или началу БИК.

        Примеры запросов:
        GET /api/cbr/search?query=Сбербанк
        GET /api/cbr/search?query=0445&limit=50

        Аргументы:
            query: Строка поиска. Если состоит только из цифр — трактуется как БИК (поиск по началу кода), иначе ищется как подстрока в наименовании, населённом пункте и SWIFT.
            limit: Максимальное количество результатов (по умолчанию 20, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CbrSearchResponse",
            await self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    async def get_stats(self, *, timeout: float | None = None) -> _types.CbrStatsResponse:
        """
        Возвращает статистику загруженного справочника: размер, дата актуальности, готовность.

        Пример запроса:
        GET /api/cbr/stats

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CbrStatsResponse", await self._client.request(_get_stats_options(timeout=timeout)))


class CbrResourceWithRawResponse:
    """Методы :class:`CbrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: CbrResource) -> None:
        self.get = to_raw_response_wrapper(resource.get)
        self.search = to_raw_response_wrapper(resource.search)
        self.get_stats = to_raw_response_wrapper(resource.get_stats)


class AsyncCbrResourceWithRawResponse:
    """Методы :class:`AsyncCbrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncCbrResource) -> None:
        self.get = to_async_raw_response_wrapper(resource.get)
        self.search = to_async_raw_response_wrapper(resource.search)
        self.get_stats = to_async_raw_response_wrapper(resource.get_stats)
