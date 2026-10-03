"""
Ресурс «API валидации телефона»: ``client.phone``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import phone as _types

__all__ = ["AsyncPhoneResource", "PhoneResource"]


def _validate_options(*, number: str, country_code: str | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path=f"/api/phone/{path_segment(number)}", params={"countryCode": country_code}, timeout=timeout
    )


class PhoneResource(SyncAPIResource):
    """
    API валидации телефона.

    Примеры на шести языках: https://github.com/atlorium-api/phone-validation-api-client
    """

    @cached_property
    def with_raw_response(self) -> PhoneResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return PhoneResourceWithRawResponse(self)

    def validate(
        self, number: str, *, country_code: str | None = None, timeout: float | None = None
    ) -> _types.PhoneReport:
        """
        Возвращает карточку телефонного номера: валидность, форматы записи, страну, тип номера,
        оператора диапазона, регион и часовые пояса.

        Примеры запросов:
        GET /api/phone/%2B79161234567
        GET /api/phone/89161234567?countryCode=RU

        ЧТО ЗНАЧИТ isValid. Номер записан правильно и попадает в диапазон, реально выделенный
        в его стране. Это НЕ означает, что номер кому-то принадлежит и что он доступен.

        ЧТО ЗНАЧИТ originalCarrier. Оператор, которому ВЫДЕЛЕН диапазон номера. Абонент вправе
        перенести номер к другому оператору, сохранив его (MNP), и справочник нумерации об этом
        не знает. Для произвольного номера это поле — обоснованная догадка, а не факт.

        Аргументы:
            number: Номер телефона. Принимается в международном формате ("+79161234567") или в национальном ("8 916 123-45-67") — во втором случае обязательно укажите countryCode. Пробелы, скобки и дефисы допустимы. Знак «+» в URL кодируется как %2B.
            country_code: Код страны (ISO-3166 alpha-2, например "RU"), в которой трактовать номер, записанный в национальном формате. Для номеров с «+» не нужен и игнорируется.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.PhoneReport",
            self._client.request(_validate_options(number=number, country_code=country_code, timeout=timeout)),
        )


class AsyncPhoneResource(AsyncAPIResource):
    """
    API валидации телефона.

    Примеры на шести языках: https://github.com/atlorium-api/phone-validation-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncPhoneResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncPhoneResourceWithRawResponse(self)

    async def validate(
        self, number: str, *, country_code: str | None = None, timeout: float | None = None
    ) -> _types.PhoneReport:
        """
        Возвращает карточку телефонного номера: валидность, форматы записи, страну, тип номера,
        оператора диапазона, регион и часовые пояса.

        Примеры запросов:
        GET /api/phone/%2B79161234567
        GET /api/phone/89161234567?countryCode=RU

        ЧТО ЗНАЧИТ isValid. Номер записан правильно и попадает в диапазон, реально выделенный
        в его стране. Это НЕ означает, что номер кому-то принадлежит и что он доступен.

        ЧТО ЗНАЧИТ originalCarrier. Оператор, которому ВЫДЕЛЕН диапазон номера. Абонент вправе
        перенести номер к другому оператору, сохранив его (MNP), и справочник нумерации об этом
        не знает. Для произвольного номера это поле — обоснованная догадка, а не факт.

        Аргументы:
            number: Номер телефона. Принимается в международном формате ("+79161234567") или в национальном ("8 916 123-45-67") — во втором случае обязательно укажите countryCode. Пробелы, скобки и дефисы допустимы. Знак «+» в URL кодируется как %2B.
            country_code: Код страны (ISO-3166 alpha-2, например "RU"), в которой трактовать номер, записанный в национальном формате. Для номеров с «+» не нужен и игнорируется.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.PhoneReport",
            await self._client.request(_validate_options(number=number, country_code=country_code, timeout=timeout)),
        )


class PhoneResourceWithRawResponse:
    """Методы :class:`PhoneResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: PhoneResource) -> None:
        self.validate = to_raw_response_wrapper(resource.validate)


class AsyncPhoneResourceWithRawResponse:
    """Методы :class:`AsyncPhoneResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncPhoneResource) -> None:
        self.validate = to_async_raw_response_wrapper(resource.validate)
