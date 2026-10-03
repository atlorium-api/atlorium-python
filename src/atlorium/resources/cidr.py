"""
Ресурс «API калькулятора подсетей»: ``client.cidr``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import cidr as _types

__all__ = ["AsyncCidrResource", "CidrResource"]


def _calculate_options(*, ip: str, mask: int, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/cidr/calculate", params={"ip": ip, "mask": mask}, timeout=timeout)


def _split_options(*, cidr: str, new_mask: int, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/cidr/subnets", params={"cidr": cidr, "newMask": new_mask}, timeout=timeout
    )


def _check_options(*, cidr: str, ip: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/cidr/check", params={"cidr": cidr, "ip": ip}, timeout=timeout)


def _supernet_options(*, inputs: Sequence[str], timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/cidr/supernet",
        json=strip_none({"inputs": ensure_sequence(inputs)}),
        has_body=True,
        timeout=timeout,
    )


class CidrResource(SyncAPIResource):
    """
    API калькулятора подсетей.

    Примеры на шести языках: https://github.com/atlorium-api/cidr-subnet-calculator-api-client
    """

    @cached_property
    def with_raw_response(self) -> CidrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return CidrResourceWithRawResponse(self)

    def calculate(self, ip: str, mask: int, *, timeout: float | None = None) -> _types.CidrCalculationResult:
        """
        Вычисляет все параметры CIDR-блока.

        Пример запроса: GET /api/cidr/calculate?ip=192.168.1.0&mask=24

        Возвращает:
        - Network Address (адрес сети)
        - Broadcast Address (широковещательный адрес)
        - Netmask (маска подсети)
        - Wildcard Mask (wildcard-маска)
        - First/Last Usable IP (первый/последний используемый IP)
        - Total/Usable Hosts (общее/используемое количество хостов)
        - Binary/Hex представления

        Аргументы:
            ip: IP-адрес (IPv4 или IPv6), например: 192.168.1.0 или 2001:db8::1
            mask: Маска подсети в CIDR-нотации (0-32 для IPv4, 0-128 для IPv6)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CidrCalculationResult", self._client.request(_calculate_options(ip=ip, mask=mask, timeout=timeout))
        )

    def split(self, cidr: str, new_mask: int, *, timeout: float | None = None) -> _types.SubnetBreakdownResult:
        """
        Разбивает CIDR-блок на подсети с указанной новой маской.

        Пример запроса: GET /api/cidr/subnets?cidr=192.168.0.0/16&newMask=24

        Если количество подсетей превышает 128, возвращаются только первые 128.
        Флаг IsTruncated указывает на усечение результата.

        Аргументы:
            cidr: Исходный CIDR, например: 192.168.0.0/16
            new_mask: Новая маска для подсетей (должна быть больше текущей)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SubnetBreakdownResult",
            self._client.request(_split_options(cidr=cidr, new_mask=new_mask, timeout=timeout)),
        )

    def check(self, cidr: str, ip: str, *, timeout: float | None = None) -> _types.IpRangeCheckResult:
        """
        Проверяет, находится ли указанный IP-адрес в пределах CIDR-диапазона.

        Пример запроса: GET /api/cidr/check?cidr=10.0.0.0/8&ip=10.5.5.5

        Аргументы:
            cidr: CIDR-диапазон для проверки, например: 10.0.0.0/8
            ip: IP-адрес для проверки, например: 10.5.5.5
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.IpRangeCheckResult", self._client.request(_check_options(cidr=cidr, ip=ip, timeout=timeout))
        )

    def supernet(self, inputs: Sequence[str], *, timeout: float | None = None) -> _types.SupernetResult:
        """
        Вычисляет наименьший общий CIDR (Supernet), покрывающий все входные IP/CIDR.

        Пример запроса: POST /api/cidr/supernet
        Body: { "inputs": ["192.168.1.0/24", "192.168.2.0/24", "192.168.3.0/24"] }

        Поддерживаемые форматы входных данных:
        - CIDR: 192.168.0.0/24
        - Одиночный IP: 192.168.1.1

        Смешивание IPv4 и IPv6 не поддерживается.

        Аргументы:
            inputs: Список входных IP-адресов и/или CIDR для агрегации. Поддерживаемые разделители: новая строка, запятая, точка с запятой, пробел.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.SupernetResult", self._client.request(_supernet_options(inputs=inputs, timeout=timeout)))


class AsyncCidrResource(AsyncAPIResource):
    """
    API калькулятора подсетей.

    Примеры на шести языках: https://github.com/atlorium-api/cidr-subnet-calculator-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncCidrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncCidrResourceWithRawResponse(self)

    async def calculate(self, ip: str, mask: int, *, timeout: float | None = None) -> _types.CidrCalculationResult:
        """
        Вычисляет все параметры CIDR-блока.

        Пример запроса: GET /api/cidr/calculate?ip=192.168.1.0&mask=24

        Возвращает:
        - Network Address (адрес сети)
        - Broadcast Address (широковещательный адрес)
        - Netmask (маска подсети)
        - Wildcard Mask (wildcard-маска)
        - First/Last Usable IP (первый/последний используемый IP)
        - Total/Usable Hosts (общее/используемое количество хостов)
        - Binary/Hex представления

        Аргументы:
            ip: IP-адрес (IPv4 или IPv6), например: 192.168.1.0 или 2001:db8::1
            mask: Маска подсети в CIDR-нотации (0-32 для IPv4, 0-128 для IPv6)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CidrCalculationResult",
            await self._client.request(_calculate_options(ip=ip, mask=mask, timeout=timeout)),
        )

    async def split(self, cidr: str, new_mask: int, *, timeout: float | None = None) -> _types.SubnetBreakdownResult:
        """
        Разбивает CIDR-блок на подсети с указанной новой маской.

        Пример запроса: GET /api/cidr/subnets?cidr=192.168.0.0/16&newMask=24

        Если количество подсетей превышает 128, возвращаются только первые 128.
        Флаг IsTruncated указывает на усечение результата.

        Аргументы:
            cidr: Исходный CIDR, например: 192.168.0.0/16
            new_mask: Новая маска для подсетей (должна быть больше текущей)
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SubnetBreakdownResult",
            await self._client.request(_split_options(cidr=cidr, new_mask=new_mask, timeout=timeout)),
        )

    async def check(self, cidr: str, ip: str, *, timeout: float | None = None) -> _types.IpRangeCheckResult:
        """
        Проверяет, находится ли указанный IP-адрес в пределах CIDR-диапазона.

        Пример запроса: GET /api/cidr/check?cidr=10.0.0.0/8&ip=10.5.5.5

        Аргументы:
            cidr: CIDR-диапазон для проверки, например: 10.0.0.0/8
            ip: IP-адрес для проверки, например: 10.5.5.5
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.IpRangeCheckResult", await self._client.request(_check_options(cidr=cidr, ip=ip, timeout=timeout))
        )

    async def supernet(self, inputs: Sequence[str], *, timeout: float | None = None) -> _types.SupernetResult:
        """
        Вычисляет наименьший общий CIDR (Supernet), покрывающий все входные IP/CIDR.

        Пример запроса: POST /api/cidr/supernet
        Body: { "inputs": ["192.168.1.0/24", "192.168.2.0/24", "192.168.3.0/24"] }

        Поддерживаемые форматы входных данных:
        - CIDR: 192.168.0.0/24
        - Одиночный IP: 192.168.1.1

        Смешивание IPv4 и IPv6 не поддерживается.

        Аргументы:
            inputs: Список входных IP-адресов и/или CIDR для агрегации. Поддерживаемые разделители: новая строка, запятая, точка с запятой, пробел.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SupernetResult", await self._client.request(_supernet_options(inputs=inputs, timeout=timeout))
        )


class CidrResourceWithRawResponse:
    """Методы :class:`CidrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: CidrResource) -> None:
        self.calculate = to_raw_response_wrapper(resource.calculate)
        self.split = to_raw_response_wrapper(resource.split)
        self.check = to_raw_response_wrapper(resource.check)
        self.supernet = to_raw_response_wrapper(resource.supernet)


class AsyncCidrResourceWithRawResponse:
    """Методы :class:`AsyncCidrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncCidrResource) -> None:
        self.calculate = to_async_raw_response_wrapper(resource.calculate)
        self.split = to_async_raw_response_wrapper(resource.split)
        self.check = to_async_raw_response_wrapper(resource.check)
        self.supernet = to_async_raw_response_wrapper(resource.supernet)
