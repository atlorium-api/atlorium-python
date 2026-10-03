"""
Ресурс «API погодных данных»: ``client.weather``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import weather as _types

__all__ = ["AsyncWeatherResource", "WeatherResource"]


def _get_options(*, latitude: float, longitude: float, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/weather", params={"latitude": latitude, "longitude": longitude}, timeout=timeout
    )


class WeatherResource(SyncAPIResource):
    """
    API погодных данных.

    Примеры на шести языках: https://github.com/atlorium-api/weather-api-client
    """

    @cached_property
    def with_raw_response(self) -> WeatherResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return WeatherResourceWithRawResponse(self)

    def get(self, latitude: float, longitude: float, *, timeout: float | None = None) -> _types.WeatherData:
        """
        Получает текущие погодные данные для указанных географических координат.

        Пример запроса для Москвы:
        GET /api/weather?latitude=55.7558&longitude=37.6173

        Пример запроса для Санкт-Петербурга:
        GET /api/weather?latitude=59.9343&longitude=30.3351

        Ограничения:
        - При превышении лимита запросов возвращается код 429
        - Координаты должны быть в допустимых диапазонах

        Аргументы:
            latitude: Географическая широта в градусах (десятичный формат).  Допустимые значения: от -90.0 до +90.0 - Положительные значения: Северное полушарие (например, 55.7558 — Москва) - Отрицательные значения: Южное полушарие (например, -33.8688 — Сидней) - 0: Экватор  Примеры: 55.7558 (Москва), 51.5074 (Лондон), 40.7128 (Нью-Йорк)
            longitude: Географическая долгота в градусах (десятичный формат).  Допустимые значения: от -180.0 до +180.0 - Положительные значения: Восточное полушарие (например, 37.6173 — Москва) - Отрицательные значения: Западное полушарие (например, -74.0060 — Нью-Йорк) - 0: Нулевой меридиан (Гринвич)  Примеры: 37.6173 (Москва), -0.1278 (Лондон), -74.0060 (Нью-Йорк)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.WeatherData",
            self._client.request(_get_options(latitude=latitude, longitude=longitude, timeout=timeout)),
        )


class AsyncWeatherResource(AsyncAPIResource):
    """
    API погодных данных.

    Примеры на шести языках: https://github.com/atlorium-api/weather-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncWeatherResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncWeatherResourceWithRawResponse(self)

    async def get(self, latitude: float, longitude: float, *, timeout: float | None = None) -> _types.WeatherData:
        """
        Получает текущие погодные данные для указанных географических координат.

        Пример запроса для Москвы:
        GET /api/weather?latitude=55.7558&longitude=37.6173

        Пример запроса для Санкт-Петербурга:
        GET /api/weather?latitude=59.9343&longitude=30.3351

        Ограничения:
        - При превышении лимита запросов возвращается код 429
        - Координаты должны быть в допустимых диапазонах

        Аргументы:
            latitude: Географическая широта в градусах (десятичный формат).  Допустимые значения: от -90.0 до +90.0 - Положительные значения: Северное полушарие (например, 55.7558 — Москва) - Отрицательные значения: Южное полушарие (например, -33.8688 — Сидней) - 0: Экватор  Примеры: 55.7558 (Москва), 51.5074 (Лондон), 40.7128 (Нью-Йорк)
            longitude: Географическая долгота в градусах (десятичный формат).  Допустимые значения: от -180.0 до +180.0 - Положительные значения: Восточное полушарие (например, 37.6173 — Москва) - Отрицательные значения: Западное полушарие (например, -74.0060 — Нью-Йорк) - 0: Нулевой меридиан (Гринвич)  Примеры: 37.6173 (Москва), -0.1278 (Лондон), -74.0060 (Нью-Йорк)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.WeatherData",
            await self._client.request(_get_options(latitude=latitude, longitude=longitude, timeout=timeout)),
        )


class WeatherResourceWithRawResponse:
    """Методы :class:`WeatherResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: WeatherResource) -> None:
        self.get = to_raw_response_wrapper(resource.get)


class AsyncWeatherResourceWithRawResponse:
    """Методы :class:`AsyncWeatherResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncWeatherResource) -> None:
        self.get = to_async_raw_response_wrapper(resource.get)
