"""
Ресурс «API стандартизации адреса»: ``client.addressstd``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import addressstd as _types

__all__ = ["AddressStdResource", "AsyncAddressStdResource"]


def _standardize_options(
    *, address: str, region: int | None, bind: bool | None, geocode: bool | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/addressstd",
        params={"address": address, "region": region, "bind": bind, "geocode": geocode},
        timeout=timeout,
    )


class AddressStdResource(SyncAPIResource):
    """
    API стандартизации адреса.

    Примеры на шести языках: https://github.com/atlorium-api/address-standardization-api-client
    """

    @cached_property
    def with_raw_response(self) -> AddressStdResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AddressStdResourceWithRawResponse(self)

    def standardize(
        self,
        address: str,
        *,
        region: int | None = None,
        bind: bool | None = None,
        geocode: bool | None = None,
        timeout: float | None = None,
    ) -> _types.StandardizedAddress:
        """
        Разбирает адресную строку в структуру: адресные уровни (регион/город/улица/дом/квартира),
        нормализованное однострочное представление и коэффициент качества.

        Примеры запросов:
        GET /api/addressstd?address=г Москва, ул. 16-я Парковая д.2 к1 кв.3
        GET /api/addressstd?address=ленинский проспект 4&region=77

        Аргументы:
            address: Адресная строка. Примеры: «мск ленинскй проспект д4 кв5», «г Москва, ул. 16-я Парковая д.2 к1 кв.3». Допускаются опечатки, сокращения, нижний регистр и переставленные части.
            region: Код региона по умолчанию (2 цифры, например 77), если в строке регион не указан — помогает разобрать «улица + дом» без верхнего уровня. Необязателен.
            bind: Дополнить разбор привязкой к государственному адресному реестру (ГАР/ФИАС). Режим готовится к запуску: сейчас запрос с этим флагом возвращает 501 и не тарифицируется. После запуска будет тарифицироваться дополнительно к базовому разбору.
            geocode: Дополнить разбор географическими координатами адреса. Режим готовится к запуску: сейчас запрос с этим флагом возвращает 501 и не тарифицируется. После запуска будет тарифицироваться дополнительно к базовому разбору.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.StandardizedAddress",
            self._client.request(
                _standardize_options(address=address, region=region, bind=bind, geocode=geocode, timeout=timeout)
            ),
        )


class AsyncAddressStdResource(AsyncAPIResource):
    """
    API стандартизации адреса.

    Примеры на шести языках: https://github.com/atlorium-api/address-standardization-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncAddressStdResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncAddressStdResourceWithRawResponse(self)

    async def standardize(
        self,
        address: str,
        *,
        region: int | None = None,
        bind: bool | None = None,
        geocode: bool | None = None,
        timeout: float | None = None,
    ) -> _types.StandardizedAddress:
        """
        Разбирает адресную строку в структуру: адресные уровни (регион/город/улица/дом/квартира),
        нормализованное однострочное представление и коэффициент качества.

        Примеры запросов:
        GET /api/addressstd?address=г Москва, ул. 16-я Парковая д.2 к1 кв.3
        GET /api/addressstd?address=ленинский проспект 4&region=77

        Аргументы:
            address: Адресная строка. Примеры: «мск ленинскй проспект д4 кв5», «г Москва, ул. 16-я Парковая д.2 к1 кв.3». Допускаются опечатки, сокращения, нижний регистр и переставленные части.
            region: Код региона по умолчанию (2 цифры, например 77), если в строке регион не указан — помогает разобрать «улица + дом» без верхнего уровня. Необязателен.
            bind: Дополнить разбор привязкой к государственному адресному реестру (ГАР/ФИАС). Режим готовится к запуску: сейчас запрос с этим флагом возвращает 501 и не тарифицируется. После запуска будет тарифицироваться дополнительно к базовому разбору.
            geocode: Дополнить разбор географическими координатами адреса. Режим готовится к запуску: сейчас запрос с этим флагом возвращает 501 и не тарифицируется. После запуска будет тарифицироваться дополнительно к базовому разбору.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.StandardizedAddress",
            await self._client.request(
                _standardize_options(address=address, region=region, bind=bind, geocode=geocode, timeout=timeout)
            ),
        )


class AddressStdResourceWithRawResponse:
    """Методы :class:`AddressStdResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AddressStdResource) -> None:
        self.standardize = to_raw_response_wrapper(resource.standardize)


class AsyncAddressStdResourceWithRawResponse:
    """Методы :class:`AsyncAddressStdResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncAddressStdResource) -> None:
        self.standardize = to_async_raw_response_wrapper(resource.standardize)
