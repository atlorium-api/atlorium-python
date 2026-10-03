"""
Ресурс «API BIN Lookup»: ``client.bin``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import bin as _types

__all__ = ["AsyncBinResource", "BinResource"]


def _lookup_options(*, bin: str, customer_ip: str | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path=f"/api/bin/{path_segment(bin)}", params={"customerIp": customer_ip}, timeout=timeout
    )


def _validate_options(*, bin: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/bin/validate/{path_segment(bin)}", timeout=timeout)


class BinResource(SyncAPIResource):
    """
    API BIN Lookup.

    Примеры на шести языках: https://github.com/atlorium-api/bin-lookup-api-client
    """

    @cached_property
    def with_raw_response(self) -> BinResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return BinResourceWithRawResponse(self)

    def lookup(
        self, bin: str, *, customer_ip: str | None = None, timeout: float | None = None
    ) -> _types.BinLookupResult:
        """
        Возвращает карточку по BIN/IIN (6, 8 или 10 цифр). Для максимальной точности
        рекомендуется передавать 8 и более цифр.

        Примеры запросов:
        GET /api/bin/48334884
        GET /api/bin/48334884?customerIp=8.8.8.8

        Аргументы:
            bin: BIN/IIN — первые 6, 8 или 10 цифр номера карты. Пример: 48334884.
            customer_ip: (Необязательно) IP-адрес клиента. Если передан — в ответ добавятся антифрод-данные по IP (страна/город, совпадение страны IP со страной карты, проверка по спискам блокировок).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.BinLookupResult",
            self._client.request(_lookup_options(bin=bin, customer_ip=customer_ip, timeout=timeout)),
        )

    def validate(self, bin: str, *, timeout: float | None = None) -> _types.BinFormatValidationResult:
        """
        Мгновенно проверяет формат BIN/IIN (только цифры, длина 6, 8 или 10).
        Проверяет формат, а не существование такого BIN.

        Пример запроса:
        GET /api/bin/validate/48334884

        Аргументы:
            bin: Проверяемый BIN (6, 8 или 10 цифр; пробелы/разделители игнорируются).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.BinFormatValidationResult", self._client.request(_validate_options(bin=bin, timeout=timeout))
        )


class AsyncBinResource(AsyncAPIResource):
    """
    API BIN Lookup.

    Примеры на шести языках: https://github.com/atlorium-api/bin-lookup-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncBinResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncBinResourceWithRawResponse(self)

    async def lookup(
        self, bin: str, *, customer_ip: str | None = None, timeout: float | None = None
    ) -> _types.BinLookupResult:
        """
        Возвращает карточку по BIN/IIN (6, 8 или 10 цифр). Для максимальной точности
        рекомендуется передавать 8 и более цифр.

        Примеры запросов:
        GET /api/bin/48334884
        GET /api/bin/48334884?customerIp=8.8.8.8

        Аргументы:
            bin: BIN/IIN — первые 6, 8 или 10 цифр номера карты. Пример: 48334884.
            customer_ip: (Необязательно) IP-адрес клиента. Если передан — в ответ добавятся антифрод-данные по IP (страна/город, совпадение страны IP со страной карты, проверка по спискам блокировок).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.BinLookupResult",
            await self._client.request(_lookup_options(bin=bin, customer_ip=customer_ip, timeout=timeout)),
        )

    async def validate(self, bin: str, *, timeout: float | None = None) -> _types.BinFormatValidationResult:
        """
        Мгновенно проверяет формат BIN/IIN (только цифры, длина 6, 8 или 10).
        Проверяет формат, а не существование такого BIN.

        Пример запроса:
        GET /api/bin/validate/48334884

        Аргументы:
            bin: Проверяемый BIN (6, 8 или 10 цифр; пробелы/разделители игнорируются).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.BinFormatValidationResult", await self._client.request(_validate_options(bin=bin, timeout=timeout))
        )


class BinResourceWithRawResponse:
    """Методы :class:`BinResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: BinResource) -> None:
        self.lookup = to_raw_response_wrapper(resource.lookup)
        self.validate = to_raw_response_wrapper(resource.validate)


class AsyncBinResourceWithRawResponse:
    """Методы :class:`AsyncBinResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncBinResource) -> None:
        self.lookup = to_async_raw_response_wrapper(resource.lookup)
        self.validate = to_async_raw_response_wrapper(resource.validate)
