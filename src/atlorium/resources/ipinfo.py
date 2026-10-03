"""
Ресурс «API профиля IP»: ``client.ipinfo``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import ipinfo as _types

__all__ = ["AsyncIpInfoResource", "IpInfoResource"]


def _lookup_options(*, ip: str, extended: bool | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path=f"/api/ipinfo/{path_segment(ip)}", params={"extended": extended}, timeout=timeout
    )


class IpInfoResource(SyncAPIResource):
    """
    API профиля IP.

    Примеры на шести языках: https://github.com/atlorium-api/ip-geolocation-api-client
    """

    @cached_property
    def with_raw_response(self) -> IpInfoResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return IpInfoResourceWithRawResponse(self)

    def lookup(self, ip: str, *, extended: bool | None = None, timeout: float | None = None) -> _types.IpReport:
        """
        Возвращает профиль IP-адреса: геолокацию, а при extended=true — ещё и сведения о владельце
        и репутации адреса.

        Примеры запросов:
        GET /api/ipinfo/8.8.8.8
        GET /api/ipinfo/206.189.233.36?extended=true

        Аргументы:
            ip: IP-адрес (IPv4 или IPv6). Примеры: 8.8.8.8, 2606:4700:4700::1111. Приватные и зарезервированные адреса публичного профиля не имеют.
            extended: Расширенные сведения: владелец сети (ASN/организация), hostname, признаки анонимизации (VPN/прокси/Tor/relay/резидентный прокси), контакт для жалоб и отметка о жалобах. По умолчанию false. Расширенный режим тарифицируется по собственной цене — см. страницу тарифов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.IpReport", self._client.request(_lookup_options(ip=ip, extended=extended, timeout=timeout)))


class AsyncIpInfoResource(AsyncAPIResource):
    """
    API профиля IP.

    Примеры на шести языках: https://github.com/atlorium-api/ip-geolocation-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncIpInfoResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncIpInfoResourceWithRawResponse(self)

    async def lookup(self, ip: str, *, extended: bool | None = None, timeout: float | None = None) -> _types.IpReport:
        """
        Возвращает профиль IP-адреса: геолокацию, а при extended=true — ещё и сведения о владельце
        и репутации адреса.

        Примеры запросов:
        GET /api/ipinfo/8.8.8.8
        GET /api/ipinfo/206.189.233.36?extended=true

        Аргументы:
            ip: IP-адрес (IPv4 или IPv6). Примеры: 8.8.8.8, 2606:4700:4700::1111. Приватные и зарезервированные адреса публичного профиля не имеют.
            extended: Расширенные сведения: владелец сети (ASN/организация), hostname, признаки анонимизации (VPN/прокси/Tor/relay/резидентный прокси), контакт для жалоб и отметка о жалобах. По умолчанию false. Расширенный режим тарифицируется по собственной цене — см. страницу тарифов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.IpReport", await self._client.request(_lookup_options(ip=ip, extended=extended, timeout=timeout))
        )


class IpInfoResourceWithRawResponse:
    """Методы :class:`IpInfoResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: IpInfoResource) -> None:
        self.lookup = to_raw_response_wrapper(resource.lookup)


class AsyncIpInfoResourceWithRawResponse:
    """Методы :class:`AsyncIpInfoResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncIpInfoResource) -> None:
        self.lookup = to_async_raw_response_wrapper(resource.lookup)
