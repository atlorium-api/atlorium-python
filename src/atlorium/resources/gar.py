"""
Ресурс «ГАР/ФИАС API»: ``client.gar``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import gar as _types

__all__ = ["AsyncGarResource", "GarResource"]


def _search_options(*, query: str, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/gar/search", params={"query": query, "limit": limit}, timeout=timeout
    )


def _suggest_options(*, query: str, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/gar/suggest", params={"query": query, "limit": limit}, timeout=timeout
    )


def _get_object_options(*, guid: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/gar/object/{path_segment(guid)}", timeout=timeout)


def _get_object_by_id_options(*, object_id: int, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/gar/object/id/{path_segment(object_id)}", timeout=timeout)


def _get_children_options(*, parent_object_id: int, limit: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path=f"/api/gar/children/{path_segment(parent_object_id)}",
        params={"limit": limit},
        timeout=timeout,
    )


def _get_hierarchy_options(*, object_id: int, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/gar/hierarchy/{path_segment(object_id)}", timeout=timeout)


def _get_stats_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/gar/stats", timeout=timeout)


def _list_regions_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/gar/regions", timeout=timeout)


def _get_region_stats_options(*, region_code: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/gar/region/{path_segment(region_code)}/stats", timeout=timeout)


class GarResource(SyncAPIResource):
    """
    ГАР/ФИАС API.

    Примеры на шести языках: https://github.com/atlorium-api/gar-fias-address-api-client
    """

    @cached_property
    def with_raw_response(self) -> GarResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return GarResourceWithRawResponse(self)

    def search(self, query: str, *, limit: int | None = None, timeout: float | None = None) -> _types.GarSearchResponse:
        """
        Ищет адресные объекты по произвольной строке запроса: разбирает её на части и
        находит регионы, населённые пункты, улицы, дома, квартиры и комнаты.

        Пример запроса:
        GET /api/gar/search?query=Москва ул Ленина д 5
        GET /api/gar/search?query=Самарская, Самара, Пушкина&limit=20

        Аргументы:
            query: Строка поиска адреса.  Формат: произвольный текст, элементы можно разделять запятыми.  Примеры: - Москва ул Ленина д 5 - Самарская обл, Самара, Ленина, д 5 кв 18 - ул Пушкина
            limit: Максимальное количество результатов (по умолчанию 10, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarSearchResponse", self._client.request(_search_options(query=query, limit=limit, timeout=timeout))
        )

    def suggest(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.GarSuggestResponse:
        """
        Возвращает подсказки автодополнения для быстрого поиска адресных объектов.
        Облегчённая версия search — возвращает только имена и идентификаторы.

        Аргументы:
            query: Строка для автодополнения (минимум 2 символа).
            limit: Максимальное количество подсказок (по умолчанию 7, максимум 20).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarSuggestResponse",
            self._client.request(_suggest_options(query=query, limit=limit, timeout=timeout)),
        )

    def get_object(self, guid: str, *, timeout: float | None = None) -> _types.GarObjectDetailsResponse:
        """
        Получает детальную информацию об объекте ГАР по его UUID (GUID).
        Включает иерархию, параметры (почтовый индекс, ОКТМО, ОКАТО, ИФНС, КЛАДР).

        Аргументы:
            guid: UUID (GUID) объекта ГАР. Формат: стандартный GUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarObjectDetailsResponse", self._client.request(_get_object_options(guid=guid, timeout=timeout))
        )

    def get_object_by_id(self, object_id: int, *, timeout: float | None = None) -> _types.GarObjectDetailsResponse:
        """
        Получает детальную информацию об объекте по числовому идентификатору (object_id).

        Аргументы:
            object_id: Числовой идентификатор объекта ГАР.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarObjectDetailsResponse",
            self._client.request(_get_object_by_id_options(object_id=object_id, timeout=timeout)),
        )

    def get_children(
        self, parent_object_id: int, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.GarChildrenResponse:
        """
        Получает список дочерних объектов для указанного родителя.
        Например: дома на улице, квартиры в доме, комнаты в квартире.

        Аргументы:
            parent_object_id: Идентификатор родительского объекта.
            limit: Максимальное количество результатов (по умолчанию 50, максимум 500).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarChildrenResponse",
            self._client.request(
                _get_children_options(parent_object_id=parent_object_id, limit=limit, timeout=timeout)
            ),
        )

    def get_hierarchy(self, object_id: int, *, timeout: float | None = None) -> _types.GarHierarchyResponse:
        """
        Получает иерархию объекта — путь от корня (региона) до указанного объекта.

        Аргументы:
            object_id: Идентификатор объекта.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarHierarchyResponse",
            self._client.request(_get_hierarchy_options(object_id=object_id, timeout=timeout)),
        )

    def get_stats(self, *, timeout: float | None = None) -> _types.GarStatsResponse:
        """
        Возвращает статистику загруженных данных ГАР:
        количество объектов по типам, загруженные регионы и состояние готовности.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.GarStatsResponse", self._client.request(_get_stats_options(timeout=timeout)))

    def list_regions(self, *, timeout: float | None = None) -> list[_types.GarRegionInfo]:
        """
        Возвращает список доступных регионов (субъектов РФ) из загруженных данных ГАР.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("list[_types.GarRegionInfo]", self._client.request(_list_regions_options(timeout=timeout)))

    def get_region_stats(self, region_code: str, *, timeout: float | None = None) -> _types.GarRegionStatsResponse:
        """
        Возвращает статистику по конкретному региону: количество объектов по типам.

        Аргументы:
            region_code: Код региона (2 цифры, например "77" = Москва).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarRegionStatsResponse",
            self._client.request(_get_region_stats_options(region_code=region_code, timeout=timeout)),
        )


class AsyncGarResource(AsyncAPIResource):
    """
    ГАР/ФИАС API.

    Примеры на шести языках: https://github.com/atlorium-api/gar-fias-address-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncGarResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncGarResourceWithRawResponse(self)

    async def search(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.GarSearchResponse:
        """
        Ищет адресные объекты по произвольной строке запроса: разбирает её на части и
        находит регионы, населённые пункты, улицы, дома, квартиры и комнаты.

        Пример запроса:
        GET /api/gar/search?query=Москва ул Ленина д 5
        GET /api/gar/search?query=Самарская, Самара, Пушкина&limit=20

        Аргументы:
            query: Строка поиска адреса.  Формат: произвольный текст, элементы можно разделять запятыми.  Примеры: - Москва ул Ленина д 5 - Самарская обл, Самара, Ленина, д 5 кв 18 - ул Пушкина
            limit: Максимальное количество результатов (по умолчанию 10, максимум 100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarSearchResponse",
            await self._client.request(_search_options(query=query, limit=limit, timeout=timeout)),
        )

    async def suggest(
        self, query: str, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.GarSuggestResponse:
        """
        Возвращает подсказки автодополнения для быстрого поиска адресных объектов.
        Облегчённая версия search — возвращает только имена и идентификаторы.

        Аргументы:
            query: Строка для автодополнения (минимум 2 символа).
            limit: Максимальное количество подсказок (по умолчанию 7, максимум 20).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarSuggestResponse",
            await self._client.request(_suggest_options(query=query, limit=limit, timeout=timeout)),
        )

    async def get_object(self, guid: str, *, timeout: float | None = None) -> _types.GarObjectDetailsResponse:
        """
        Получает детальную информацию об объекте ГАР по его UUID (GUID).
        Включает иерархию, параметры (почтовый индекс, ОКТМО, ОКАТО, ИФНС, КЛАДР).

        Аргументы:
            guid: UUID (GUID) объекта ГАР. Формат: стандартный GUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarObjectDetailsResponse",
            await self._client.request(_get_object_options(guid=guid, timeout=timeout)),
        )

    async def get_object_by_id(
        self, object_id: int, *, timeout: float | None = None
    ) -> _types.GarObjectDetailsResponse:
        """
        Получает детальную информацию об объекте по числовому идентификатору (object_id).

        Аргументы:
            object_id: Числовой идентификатор объекта ГАР.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarObjectDetailsResponse",
            await self._client.request(_get_object_by_id_options(object_id=object_id, timeout=timeout)),
        )

    async def get_children(
        self, parent_object_id: int, *, limit: int | None = None, timeout: float | None = None
    ) -> _types.GarChildrenResponse:
        """
        Получает список дочерних объектов для указанного родителя.
        Например: дома на улице, квартиры в доме, комнаты в квартире.

        Аргументы:
            parent_object_id: Идентификатор родительского объекта.
            limit: Максимальное количество результатов (по умолчанию 50, максимум 500).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarChildrenResponse",
            await self._client.request(
                _get_children_options(parent_object_id=parent_object_id, limit=limit, timeout=timeout)
            ),
        )

    async def get_hierarchy(self, object_id: int, *, timeout: float | None = None) -> _types.GarHierarchyResponse:
        """
        Получает иерархию объекта — путь от корня (региона) до указанного объекта.

        Аргументы:
            object_id: Идентификатор объекта.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarHierarchyResponse",
            await self._client.request(_get_hierarchy_options(object_id=object_id, timeout=timeout)),
        )

    async def get_stats(self, *, timeout: float | None = None) -> _types.GarStatsResponse:
        """
        Возвращает статистику загруженных данных ГАР:
        количество объектов по типам, загруженные регионы и состояние готовности.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.GarStatsResponse", await self._client.request(_get_stats_options(timeout=timeout)))

    async def list_regions(self, *, timeout: float | None = None) -> list[_types.GarRegionInfo]:
        """
        Возвращает список доступных регионов (субъектов РФ) из загруженных данных ГАР.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("list[_types.GarRegionInfo]", await self._client.request(_list_regions_options(timeout=timeout)))

    async def get_region_stats(
        self, region_code: str, *, timeout: float | None = None
    ) -> _types.GarRegionStatsResponse:
        """
        Возвращает статистику по конкретному региону: количество объектов по типам.

        Аргументы:
            region_code: Код региона (2 цифры, например "77" = Москва).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GarRegionStatsResponse",
            await self._client.request(_get_region_stats_options(region_code=region_code, timeout=timeout)),
        )


class GarResourceWithRawResponse:
    """Методы :class:`GarResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: GarResource) -> None:
        self.search = to_raw_response_wrapper(resource.search)
        self.suggest = to_raw_response_wrapper(resource.suggest)
        self.get_object = to_raw_response_wrapper(resource.get_object)
        self.get_object_by_id = to_raw_response_wrapper(resource.get_object_by_id)
        self.get_children = to_raw_response_wrapper(resource.get_children)
        self.get_hierarchy = to_raw_response_wrapper(resource.get_hierarchy)
        self.get_stats = to_raw_response_wrapper(resource.get_stats)
        self.list_regions = to_raw_response_wrapper(resource.list_regions)
        self.get_region_stats = to_raw_response_wrapper(resource.get_region_stats)


class AsyncGarResourceWithRawResponse:
    """Методы :class:`AsyncGarResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncGarResource) -> None:
        self.search = to_async_raw_response_wrapper(resource.search)
        self.suggest = to_async_raw_response_wrapper(resource.suggest)
        self.get_object = to_async_raw_response_wrapper(resource.get_object)
        self.get_object_by_id = to_async_raw_response_wrapper(resource.get_object_by_id)
        self.get_children = to_async_raw_response_wrapper(resource.get_children)
        self.get_hierarchy = to_async_raw_response_wrapper(resource.get_hierarchy)
        self.get_stats = to_async_raw_response_wrapper(resource.get_stats)
        self.list_regions = to_async_raw_response_wrapper(resource.list_regions)
        self.get_region_stats = to_async_raw_response_wrapper(resource.get_region_stats)
