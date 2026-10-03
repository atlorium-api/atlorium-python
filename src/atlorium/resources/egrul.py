"""
Ресурс «API ЕГРЮЛ/ЕГРИП»: ``client.egrul``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import egrul as _types

__all__ = ["AsyncEgrulResource", "EgrulResource"]


def _get_options(*, query: str, extended: bool | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path=f"/api/egrul/{path_segment(query)}", params={"extended": extended}, timeout=timeout
    )


def _search_options(*, query: str, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/egrul/search", params={"query": query, "limit": limit}, timeout=timeout
    )


def _get_excerpt_options(*, query: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path=f"/api/egrul/{path_segment(query)}/excerpt", timeout=timeout, response_type="bytes"
    )


class EgrulResource(SyncAPIResource):
    """
    API ЕГРЮЛ/ЕГРИП.

    Примеры на шести языках: https://github.com/atlorium-api/egrul-api-client
    """

    @cached_property
    def with_raw_response(self) -> EgrulResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return EgrulResourceWithRawResponse(self)

    def get(
        self, query: str, *, extended: bool | None = None, timeout: float | None = None
    ) -> _types.CompanyLookupResult:
        """
        Возвращает карточку организации по ИНН, ОГРН или ОГРНИП.

        Примеры запросов:
        GET /api/egrul/7707083893
        GET /api/egrul/304500116000157?extended=true

        Аргументы:
            query: Идентификатор: ИНН (10 цифр у ЮЛ, 12 у ИП), ОГРН (13 цифр) или ОГРНИП (15 цифр). Пример: 7707083893.
            extended: Расширенные сведения из официальной выписки, которых нет в базовой карточке: у ИП — адрес электронной почты и пол; у ЮЛ — состав участников/учредителей и их доли. По умолчанию false (выключено). Включение требует дополнительной обработки выписки, поэтому ответ может формироваться дольше.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CompanyLookupResult",
            self._client.request(_get_options(query=query, extended=extended, timeout=timeout)),
        )

    def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.CompanySearchResponse:
        """
        Ищет субъекты (ЮЛ и ИП) по наименованию или ФИО.

        Примеры запросов:
        GET /api/egrul/search?query=Сбербанк
        GET /api/egrul/search?query=Иванов%20Иван%20Иванович&limit=20

        Аргументы:
            query: Строка поиска: часть наименования организации или ФИО ИП. Пример: Сбербанк.
            limit: Максимум результатов (по умолчанию 10, максимум 50).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CompanySearchResponse",
            self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    def get_excerpt(self, query: str, *, timeout: float | None = None) -> bytes:
        """
        Возвращает официальную выписку из ЕГРЮЛ/ЕГРИП по идентификатору субъекта в виде PDF-файла.

        Пример запроса:
        GET /api/egrul/7707083893/excerpt

        Аргументы:
            query: ИНН, ОГРН или ОГРНИП субъекта. Пример: 7707083893.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        Возвращает содержимое файла (``bytes``).
        """
        return cast("bytes", self._client.request(_get_excerpt_options(query=query, timeout=timeout)))


class AsyncEgrulResource(AsyncAPIResource):
    """
    API ЕГРЮЛ/ЕГРИП.

    Примеры на шести языках: https://github.com/atlorium-api/egrul-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncEgrulResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncEgrulResourceWithRawResponse(self)

    async def get(
        self, query: str, *, extended: bool | None = None, timeout: float | None = None
    ) -> _types.CompanyLookupResult:
        """
        Возвращает карточку организации по ИНН, ОГРН или ОГРНИП.

        Примеры запросов:
        GET /api/egrul/7707083893
        GET /api/egrul/304500116000157?extended=true

        Аргументы:
            query: Идентификатор: ИНН (10 цифр у ЮЛ, 12 у ИП), ОГРН (13 цифр) или ОГРНИП (15 цифр). Пример: 7707083893.
            extended: Расширенные сведения из официальной выписки, которых нет в базовой карточке: у ИП — адрес электронной почты и пол; у ЮЛ — состав участников/учредителей и их доли. По умолчанию false (выключено). Включение требует дополнительной обработки выписки, поэтому ответ может формироваться дольше.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CompanyLookupResult",
            await self._client.request(_get_options(query=query, extended=extended, timeout=timeout)),
        )

    async def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.CompanySearchResponse:
        """
        Ищет субъекты (ЮЛ и ИП) по наименованию или ФИО.

        Примеры запросов:
        GET /api/egrul/search?query=Сбербанк
        GET /api/egrul/search?query=Иванов%20Иван%20Иванович&limit=20

        Аргументы:
            query: Строка поиска: часть наименования организации или ФИО ИП. Пример: Сбербанк.
            limit: Максимум результатов (по умолчанию 10, максимум 50).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CompanySearchResponse",
            await self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    async def get_excerpt(self, query: str, *, timeout: float | None = None) -> bytes:
        """
        Возвращает официальную выписку из ЕГРЮЛ/ЕГРИП по идентификатору субъекта в виде PDF-файла.

        Пример запроса:
        GET /api/egrul/7707083893/excerpt

        Аргументы:
            query: ИНН, ОГРН или ОГРНИП субъекта. Пример: 7707083893.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        Возвращает содержимое файла (``bytes``).
        """
        return cast("bytes", await self._client.request(_get_excerpt_options(query=query, timeout=timeout)))


class EgrulResourceWithRawResponse:
    """Методы :class:`EgrulResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: EgrulResource) -> None:
        self.get = to_raw_response_wrapper(resource.get)
        self.search = to_raw_response_wrapper(resource.search)
        self.get_excerpt = to_raw_response_wrapper(resource.get_excerpt)


class AsyncEgrulResourceWithRawResponse:
    """Методы :class:`AsyncEgrulResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncEgrulResource) -> None:
        self.get = to_async_raw_response_wrapper(resource.get)
        self.search = to_async_raw_response_wrapper(resource.search)
        self.get_excerpt = to_async_raw_response_wrapper(resource.get_excerpt)
