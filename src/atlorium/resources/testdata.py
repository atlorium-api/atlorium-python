"""
Ресурс «API генератора тестовых данных РФ»: ``client.testdata``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import TYPE_CHECKING, Literal, cast, overload

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import testdata as _types

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

__all__ = ["AsyncTestDataResource", "TestDataResource"]


def _generate_options(
    *,
    count: int | None,
    fields: str | Sequence[str] | None,
    seed: int | None,
    gender: _types.TestDataGender | None,
    format: Literal["json", "csv"] | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/testdata",
        params={
            "count": count,
            "fields": None if fields is None else ensure_sequence(fields),
            "seed": seed,
            "gender": gender,
            "format": format,
        },
        timeout=timeout,
        response_type="auto",
    )


def _generate_with_body_options(
    *,
    count: int | None,
    seed: int | None,
    fields: str | Sequence[str] | None,
    gender: _types.TestDataGender | None,
    format: Literal["json", "csv"] | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/testdata",
        json=strip_none(
            {
                "count": count,
                "seed": seed,
                "fields": None if fields is None else ensure_sequence(fields),
                "gender": gender,
                "format": format,
            }
        ),
        has_body=True,
        timeout=timeout,
        response_type="auto",
    )


def _list_fields_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/testdata/fields", timeout=timeout)


class TestDataResource(SyncAPIResource):
    """
    API генератора тестовых данных РФ.

    Примеры на шести языках: https://github.com/atlorium-api/test-data-generator-api-client
    """

    @cached_property
    def with_raw_response(self) -> TestDataResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return TestDataResourceWithRawResponse(self)

    @overload
    def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse: ...

    @overload
    def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["csv"],
        timeout: float | None = None,
    ) -> str: ...

    def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json", "csv"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse | str:
        """
        Генерирует набор тестовых записей. Параметры передаются в строке запроса — самый
        быстрый способ получить данные из curl, браузера или Swagger.

        Пример запроса:
        GET /api/testdata?count=5&fields=fullName,innPerson,snils&seed=42

        ТАРИФИКАЦИЯ. Списывается по одной единице за каждую сгенерированную запись.
        Отклонённый запрос (400) не тарифицируется: резерв снимается без списания.

        Аргументы:
            count: Сколько записей сгенерировать: от 1 до 100. По умолчанию 1. Это же число — стоимость запроса в единицах работы (одна запись = одна единица).
            fields: Список полей через запятую, например fullName,innPerson,snils. Если не указан, используется набор по умолчанию: ФИО, пол, дата рождения, ИНН физлица, СНИЛС, телефон, почта и адрес. Полный перечень доступных полей — GET /api/testdata/fields.
            seed: Начальное значение генератора. Одинаковый seed при одинаковых остальных параметрах даёт в точности одинаковый результат — на этом строятся стабильные автотесты. Если не задан, значение выбирается сервисом и возвращается в ответе.
            gender: Пол генерируемых персон: any (по умолчанию, выбирается случайно по каждой записи), male или female.
            format: Формат ответа: json (по умолчанию) или csv. CSV приходит плоской таблицей со строкой заголовков; использованный seed в этом случае возвращается заголовком X-Atlorium-Seed.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        При ``format="csv"`` возвращает строку CSV, иначе — разобранный JSON.
        """
        return cast(
            "_types.TestDataResponse | str",
            self._client.request(
                _generate_options(count=count, fields=fields, seed=seed, gender=gender, format=format, timeout=timeout)
            ),
        )

    @overload
    def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse: ...

    @overload
    def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["csv"],
        timeout: float | None = None,
    ) -> str: ...

    def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json", "csv"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse | str:
        """
        Генерирует набор тестовых записей по параметрам из тела запроса. Отличается от
        GET-варианта только способом передачи параметров — контракт и цена те же.

        Пример запроса:
        POST /api/testdata
        {
          "count": 5,
          "seed": 42,
          "fields": ["fullName", "innPerson", "snils"],
          "gender": "female",
          "format": "json"
        }

        Тело удобнее строки запроса, когда полей много: список приходит массивом, а не
        строкой через запятую, и не упирается в предел длины URL.

        ТАРИФИКАЦИЯ. Списывается по одной единице за каждую сгенерированную запись.

        Аргументы:
            count: Сколько записей сгенерировать. Допустимо от 1 до maxCount. Значение по умолчанию — 1.
            seed: Начальное значение генератора случайных чисел. Одинаковый seed при одинаковом наборе полей и количестве записей даёт побайтово одинаковый результат — на этом строятся стабильные автотесты.
            fields: Список полей, которые нужно сгенерировать (идентификаторы из каталога TestDataFields). Пустой список или null — будет использован набор по умолчанию default.
            gender: Пол генерируемых персон: any (по умолчанию), male или female. Влияет только на поля персоны — имя, отчество, фамилию, обращение и производные от них логин и почту.
            format: Формат ответа: json (по умолчанию) или csv. Значения из TestDataFormats.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        При ``format="csv"`` возвращает строку CSV, иначе — разобранный JSON.
        """
        return cast(
            "_types.TestDataResponse | str",
            self._client.request(
                _generate_with_body_options(
                    count=count, seed=seed, fields=fields, gender=gender, format=format, timeout=timeout
                )
            ),
        )

    def list_fields(self, *, timeout: float | None = None) -> list[_types.TestDataFieldDescriptor]:
        """
        Возвращает справочник всех типов данных, которые умеет генерировать сервис:
        идентификатор поля, название, пояснение, смысловую группу, пример значения и признак
        наличия контрольной суммы.

        Пример запроса:
        GET /api/testdata/fields

        Идентификаторы из этого справочника передаются в параметре fields запроса
        генерации. Справочник — часть контракта: если поле есть здесь, его можно запросить.

        ТАРИФИКАЦИЯ. Запрос БЕСПЛАТНЫЙ: справочник описывает контракт сервиса, а не является
        результатом его работы. Ограничение частоты запросов на него действует общее.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("list[_types.TestDataFieldDescriptor]", self._client.request(_list_fields_options(timeout=timeout)))


class AsyncTestDataResource(AsyncAPIResource):
    """
    API генератора тестовых данных РФ.

    Примеры на шести языках: https://github.com/atlorium-api/test-data-generator-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncTestDataResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncTestDataResourceWithRawResponse(self)

    @overload
    async def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse: ...

    @overload
    async def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["csv"],
        timeout: float | None = None,
    ) -> str: ...

    async def generate(
        self,
        *,
        count: int | None = None,
        fields: str | Sequence[str] | None = None,
        seed: int | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json", "csv"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse | str:
        """
        Генерирует набор тестовых записей. Параметры передаются в строке запроса — самый
        быстрый способ получить данные из curl, браузера или Swagger.

        Пример запроса:
        GET /api/testdata?count=5&fields=fullName,innPerson,snils&seed=42

        ТАРИФИКАЦИЯ. Списывается по одной единице за каждую сгенерированную запись.
        Отклонённый запрос (400) не тарифицируется: резерв снимается без списания.

        Аргументы:
            count: Сколько записей сгенерировать: от 1 до 100. По умолчанию 1. Это же число — стоимость запроса в единицах работы (одна запись = одна единица).
            fields: Список полей через запятую, например fullName,innPerson,snils. Если не указан, используется набор по умолчанию: ФИО, пол, дата рождения, ИНН физлица, СНИЛС, телефон, почта и адрес. Полный перечень доступных полей — GET /api/testdata/fields.
            seed: Начальное значение генератора. Одинаковый seed при одинаковых остальных параметрах даёт в точности одинаковый результат — на этом строятся стабильные автотесты. Если не задан, значение выбирается сервисом и возвращается в ответе.
            gender: Пол генерируемых персон: any (по умолчанию, выбирается случайно по каждой записи), male или female.
            format: Формат ответа: json (по умолчанию) или csv. CSV приходит плоской таблицей со строкой заголовков; использованный seed в этом случае возвращается заголовком X-Atlorium-Seed.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        При ``format="csv"`` возвращает строку CSV, иначе — разобранный JSON.
        """
        return cast(
            "_types.TestDataResponse | str",
            await self._client.request(
                _generate_options(count=count, fields=fields, seed=seed, gender=gender, format=format, timeout=timeout)
            ),
        )

    @overload
    async def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse: ...

    @overload
    async def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["csv"],
        timeout: float | None = None,
    ) -> str: ...

    async def generate_with_body(
        self,
        *,
        count: int | None = None,
        seed: int | None = None,
        fields: str | Sequence[str] | None = None,
        gender: _types.TestDataGender | None = None,
        format: Literal["json", "csv"] | None = None,
        timeout: float | None = None,
    ) -> _types.TestDataResponse | str:
        """
        Генерирует набор тестовых записей по параметрам из тела запроса. Отличается от
        GET-варианта только способом передачи параметров — контракт и цена те же.

        Пример запроса:
        POST /api/testdata
        {
          "count": 5,
          "seed": 42,
          "fields": ["fullName", "innPerson", "snils"],
          "gender": "female",
          "format": "json"
        }

        Тело удобнее строки запроса, когда полей много: список приходит массивом, а не
        строкой через запятую, и не упирается в предел длины URL.

        ТАРИФИКАЦИЯ. Списывается по одной единице за каждую сгенерированную запись.

        Аргументы:
            count: Сколько записей сгенерировать. Допустимо от 1 до maxCount. Значение по умолчанию — 1.
            seed: Начальное значение генератора случайных чисел. Одинаковый seed при одинаковом наборе полей и количестве записей даёт побайтово одинаковый результат — на этом строятся стабильные автотесты.
            fields: Список полей, которые нужно сгенерировать (идентификаторы из каталога TestDataFields). Пустой список или null — будет использован набор по умолчанию default.
            gender: Пол генерируемых персон: any (по умолчанию), male или female. Влияет только на поля персоны — имя, отчество, фамилию, обращение и производные от них логин и почту.
            format: Формат ответа: json (по умолчанию) или csv. Значения из TestDataFormats.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).

        При ``format="csv"`` возвращает строку CSV, иначе — разобранный JSON.
        """
        return cast(
            "_types.TestDataResponse | str",
            await self._client.request(
                _generate_with_body_options(
                    count=count, seed=seed, fields=fields, gender=gender, format=format, timeout=timeout
                )
            ),
        )

    async def list_fields(self, *, timeout: float | None = None) -> list[_types.TestDataFieldDescriptor]:
        """
        Возвращает справочник всех типов данных, которые умеет генерировать сервис:
        идентификатор поля, название, пояснение, смысловую группу, пример значения и признак
        наличия контрольной суммы.

        Пример запроса:
        GET /api/testdata/fields

        Идентификаторы из этого справочника передаются в параметре fields запроса
        генерации. Справочник — часть контракта: если поле есть здесь, его можно запросить.

        ТАРИФИКАЦИЯ. Запрос БЕСПЛАТНЫЙ: справочник описывает контракт сервиса, а не является
        результатом его работы. Ограничение частоты запросов на него действует общее.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "list[_types.TestDataFieldDescriptor]", await self._client.request(_list_fields_options(timeout=timeout))
        )


class TestDataResourceWithRawResponse:
    """Методы :class:`TestDataResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: TestDataResource) -> None:
        self.generate = to_raw_response_wrapper(cast("Callable[..., _types.TestDataResponse | str]", resource.generate))
        self.generate_with_body = to_raw_response_wrapper(
            cast("Callable[..., _types.TestDataResponse | str]", resource.generate_with_body)
        )
        self.list_fields = to_raw_response_wrapper(resource.list_fields)


class AsyncTestDataResourceWithRawResponse:
    """Методы :class:`AsyncTestDataResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncTestDataResource) -> None:
        self.generate = to_async_raw_response_wrapper(
            cast("Callable[..., Awaitable[_types.TestDataResponse | str]]", resource.generate)
        )
        self.generate_with_body = to_async_raw_response_wrapper(
            cast("Callable[..., Awaitable[_types.TestDataResponse | str]]", resource.generate_with_body)
        )
        self.list_fields = to_async_raw_response_wrapper(resource.list_fields)
