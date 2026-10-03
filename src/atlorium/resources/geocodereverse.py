"""
Ресурс «API обратного геокодинга»: ``client.geocodereverse``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import geocodereverse as _types

__all__ = ["AsyncGeocodeReverseResource", "GeocodeReverseResource"]


def _lookup_options(
    *,
    lat: float,
    lon: float,
    include_neighbors: bool | None,
    neighbors_size: int | None,
    include_admin: bool | None,
    include_nearby: bool | None,
    nearby_radius_km: float | None,
    nearby_size: int | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/geocodereverse",
        params={
            "lat": lat,
            "lon": lon,
            "includeNeighbors": include_neighbors,
            "neighborsSize": neighbors_size,
            "includeAdmin": include_admin,
            "includeNearby": include_nearby,
            "nearbyRadiusKm": nearby_radius_km,
            "nearbySize": nearby_size,
        },
        timeout=timeout,
    )


def _nearby_options(
    *, lat: float, lon: float, radius_km: float | None, size: int | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/geocodereverse/nearby",
        params={"lat": lat, "lon": lon, "radiusKm": radius_km, "size": size},
        timeout=timeout,
    )


class GeocodeReverseResource(SyncAPIResource):
    """
    API обратного геокодинга.

    Примеры на шести языках: https://github.com/atlorium-api/reverse-geocoding-api-client
    """

    @cached_property
    def with_raw_response(self) -> GeocodeReverseResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return GeocodeReverseResourceWithRawResponse(self)

    def lookup(
        self,
        lat: float,
        lon: float,
        *,
        include_neighbors: bool | None = None,
        neighbors_size: int | None = None,
        include_admin: bool | None = None,
        include_nearby: bool | None = None,
        nearby_radius_km: float | None = None,
        nearby_size: int | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeReverseResponse:
        """
        Находит ближайший адрес по координатам и добавляет запрошенные обогащения.

        Пример простого запроса (одна единица работы):
        GET /api/geocodereverse?lat=55.788226&lon=49.121984

        Пример с обогащениями (до четырёх единиц работы):
        GET /api/geocodereverse?lat=55.788226&lon=49.121984&includeNeighbors=true&includeAdmin=true&includeNearby=true

        ЗАЧЕМ СОСЕДНИЕ ДОМА. Ответом на вопрос «какой здесь адрес» является ОДИН объект —
        ближайший. Но точка нередко стоит между двумя зданиями или у торца длинного дома, и
        автоматический выбор в этом случае спорный. Соседи дают возможность разрешить сомнение
        вручную, не делая второй запрос с другим радиусом.

        ЗАЧЕМ ПРИНАДЛЕЖНОСТЬ ПО ГРАНИЦАМ. Она считается попаданием точки в полигон, а не
        выводится из найденного дома. Разница принципиальна: иначе точка в чистом поле
        унаследовала бы район ближайшей деревни за двадцать километров.

        ЧТО ВЕРНЁТСЯ ПРИ ПУСТОМ ОБОГАЩЕНИИ. Поле просто не заполняется, а единица работы за него
        не списывается: запрос остаётся успешным, потому что базовый ответ — адрес — получен.

        ТАРИФИКАЦИЯ. Смотрите поле billedUnits в ответе: в нём ровно то число, которое списано.

        Аргументы:
            lat: Широта в градусах. Для России — примерно от 41 до 82.
            lon: Долгота в градусах.
            include_neighbors: Вернуть также следующие по близости дома. Добавляет одну единицу работы.
            neighbors_size: Сколько соседних домов вернуть. Действует только вместе с includeNeighbors.
            include_admin: Вернуть административные образования, внутри границ которых лежит точка. Добавляет одну единицу работы.
            include_nearby: Вернуть ориентиры вокруг точки: магазины, аптеки, остановки. Добавляет одну единицу работы.
            nearby_radius_km: Радиус поиска ориентиров в километрах. Действует только вместе с includeNearby.
            nearby_size: Сколько ориентиров вернуть. Действует только вместе с includeNearby.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeReverseResponse",
            self._client.request(
                _lookup_options(
                    lat=lat,
                    lon=lon,
                    include_neighbors=include_neighbors,
                    neighbors_size=neighbors_size,
                    include_admin=include_admin,
                    include_nearby=include_nearby,
                    nearby_radius_km=nearby_radius_km,
                    nearby_size=nearby_size,
                    timeout=timeout,
                )
            ),
        )

    def nearby(
        self,
        lat: float,
        lon: float,
        *,
        radius_km: float | None = None,
        size: int | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeNearbyResponse:
        """
        Возвращает ориентиры вокруг точки: магазины, аптеки, остановки, заправки.

        Пример запроса:
        GET /api/geocodereverse/nearby?lat=55.788226&lon=49.121984&radiusKm=1&size=10

        ЭТО НЕ ПЕРЕЧИСЛЕНИЕ СОСЕДНИХ ДОМОВ. Режим отвечает на вопрос «что здесь есть»:
        организации и объекты городской среды. Соседние дома — это обогащение обратного
        геокодинга (параметр includeNeighbors), и стоит оно по-другому.

        ⚠ ПОЛНОТА НЕ ГАРАНТИРУЕТСЯ, и это принципиально. Сведения об объектах наносят на карту
        добровольцы: в крупных городах покрытие плотное, в малых населённых пунктах и вдоль
        трасс — разреженное. Отсутствие объекта в ответе НЕ означает, что его нет в
        действительности. Предупреждение об этом едет в каждом успешном ответе полем
        completenessNotice — показывайте его пользователю, иначе он сделает неверный вывод.

        ПОЧЕМУ РАДИУС ОГРАНИЧЕН ДЕСЯТЬЮ КИЛОМЕТРАМИ. Граница смысловая, а не техническая: запрос
        с радиусом в сотню километров — это уже не «что рядом», а постраничная выгрузка куска
        карты.

        ТАРИФИКАЦИЯ. Одна единица работы за запрос. Пустой результат (404) не тарифицируется.

        Аргументы:
            lat: Широта центра поиска в градусах.
            lon: Долгота центра поиска в градусах.
            radius_km: Радиус поиска в километрах. Максимум — 10.
            size: Сколько объектов вернуть.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeNearbyResponse",
            self._client.request(_nearby_options(lat=lat, lon=lon, radius_km=radius_km, size=size, timeout=timeout)),
        )


class AsyncGeocodeReverseResource(AsyncAPIResource):
    """
    API обратного геокодинга.

    Примеры на шести языках: https://github.com/atlorium-api/reverse-geocoding-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncGeocodeReverseResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncGeocodeReverseResourceWithRawResponse(self)

    async def lookup(
        self,
        lat: float,
        lon: float,
        *,
        include_neighbors: bool | None = None,
        neighbors_size: int | None = None,
        include_admin: bool | None = None,
        include_nearby: bool | None = None,
        nearby_radius_km: float | None = None,
        nearby_size: int | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeReverseResponse:
        """
        Находит ближайший адрес по координатам и добавляет запрошенные обогащения.

        Пример простого запроса (одна единица работы):
        GET /api/geocodereverse?lat=55.788226&lon=49.121984

        Пример с обогащениями (до четырёх единиц работы):
        GET /api/geocodereverse?lat=55.788226&lon=49.121984&includeNeighbors=true&includeAdmin=true&includeNearby=true

        ЗАЧЕМ СОСЕДНИЕ ДОМА. Ответом на вопрос «какой здесь адрес» является ОДИН объект —
        ближайший. Но точка нередко стоит между двумя зданиями или у торца длинного дома, и
        автоматический выбор в этом случае спорный. Соседи дают возможность разрешить сомнение
        вручную, не делая второй запрос с другим радиусом.

        ЗАЧЕМ ПРИНАДЛЕЖНОСТЬ ПО ГРАНИЦАМ. Она считается попаданием точки в полигон, а не
        выводится из найденного дома. Разница принципиальна: иначе точка в чистом поле
        унаследовала бы район ближайшей деревни за двадцать километров.

        ЧТО ВЕРНЁТСЯ ПРИ ПУСТОМ ОБОГАЩЕНИИ. Поле просто не заполняется, а единица работы за него
        не списывается: запрос остаётся успешным, потому что базовый ответ — адрес — получен.

        ТАРИФИКАЦИЯ. Смотрите поле billedUnits в ответе: в нём ровно то число, которое списано.

        Аргументы:
            lat: Широта в градусах. Для России — примерно от 41 до 82.
            lon: Долгота в градусах.
            include_neighbors: Вернуть также следующие по близости дома. Добавляет одну единицу работы.
            neighbors_size: Сколько соседних домов вернуть. Действует только вместе с includeNeighbors.
            include_admin: Вернуть административные образования, внутри границ которых лежит точка. Добавляет одну единицу работы.
            include_nearby: Вернуть ориентиры вокруг точки: магазины, аптеки, остановки. Добавляет одну единицу работы.
            nearby_radius_km: Радиус поиска ориентиров в километрах. Действует только вместе с includeNearby.
            nearby_size: Сколько ориентиров вернуть. Действует только вместе с includeNearby.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeReverseResponse",
            await self._client.request(
                _lookup_options(
                    lat=lat,
                    lon=lon,
                    include_neighbors=include_neighbors,
                    neighbors_size=neighbors_size,
                    include_admin=include_admin,
                    include_nearby=include_nearby,
                    nearby_radius_km=nearby_radius_km,
                    nearby_size=nearby_size,
                    timeout=timeout,
                )
            ),
        )

    async def nearby(
        self,
        lat: float,
        lon: float,
        *,
        radius_km: float | None = None,
        size: int | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeNearbyResponse:
        """
        Возвращает ориентиры вокруг точки: магазины, аптеки, остановки, заправки.

        Пример запроса:
        GET /api/geocodereverse/nearby?lat=55.788226&lon=49.121984&radiusKm=1&size=10

        ЭТО НЕ ПЕРЕЧИСЛЕНИЕ СОСЕДНИХ ДОМОВ. Режим отвечает на вопрос «что здесь есть»:
        организации и объекты городской среды. Соседние дома — это обогащение обратного
        геокодинга (параметр includeNeighbors), и стоит оно по-другому.

        ⚠ ПОЛНОТА НЕ ГАРАНТИРУЕТСЯ, и это принципиально. Сведения об объектах наносят на карту
        добровольцы: в крупных городах покрытие плотное, в малых населённых пунктах и вдоль
        трасс — разреженное. Отсутствие объекта в ответе НЕ означает, что его нет в
        действительности. Предупреждение об этом едет в каждом успешном ответе полем
        completenessNotice — показывайте его пользователю, иначе он сделает неверный вывод.

        ПОЧЕМУ РАДИУС ОГРАНИЧЕН ДЕСЯТЬЮ КИЛОМЕТРАМИ. Граница смысловая, а не техническая: запрос
        с радиусом в сотню километров — это уже не «что рядом», а постраничная выгрузка куска
        карты.

        ТАРИФИКАЦИЯ. Одна единица работы за запрос. Пустой результат (404) не тарифицируется.

        Аргументы:
            lat: Широта центра поиска в градусах.
            lon: Долгота центра поиска в градусах.
            radius_km: Радиус поиска в километрах. Максимум — 10.
            size: Сколько объектов вернуть.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeNearbyResponse",
            await self._client.request(
                _nearby_options(lat=lat, lon=lon, radius_km=radius_km, size=size, timeout=timeout)
            ),
        )


class GeocodeReverseResourceWithRawResponse:
    """Методы :class:`GeocodeReverseResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: GeocodeReverseResource) -> None:
        self.lookup = to_raw_response_wrapper(resource.lookup)
        self.nearby = to_raw_response_wrapper(resource.nearby)


class AsyncGeocodeReverseResourceWithRawResponse:
    """Методы :class:`AsyncGeocodeReverseResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncGeocodeReverseResource) -> None:
        self.lookup = to_async_raw_response_wrapper(resource.lookup)
        self.nearby = to_async_raw_response_wrapper(resource.nearby)
