"""
Ресурс «API прямого геокодинга»: ``client.geocodeforward``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import geocodeforward as _types

__all__ = ["AsyncGeocodeForwardResource", "GeocodeForwardResource"]


def _search_options(*, text: str, size: int | None, exact_only: bool | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/geocodeforward",
        params={"text": text, "size": size, "exactOnly": exact_only},
        timeout=timeout,
    )


def _search_structured_options(
    *,
    address: str | None,
    locality: str | None,
    region: str | None,
    postal_code: str | None,
    size: int | None,
    exact_only: bool | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/geocodeforward/structured",
        params={
            "address": address,
            "locality": locality,
            "region": region,
            "postalCode": postal_code,
            "size": size,
            "exactOnly": exact_only,
        },
        timeout=timeout,
    )


def _search_batch_options(
    *, queries: Sequence[str], size_per_query: int | None, exact_only: bool | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/geocodeforward/batch",
        json=strip_none({"queries": ensure_sequence(queries), "sizePerQuery": size_per_query, "exactOnly": exact_only}),
        has_body=True,
        timeout=timeout,
    )


def _get_place_options(*, place_id: str, include_boundary: bool | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/geocodeforward/place",
        params={"placeId": place_id, "includeBoundary": include_boundary},
        timeout=timeout,
    )


def _search_postcode_options(*, code: str, size: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/geocodeforward/postcode", params={"code": code, "size": size}, timeout=timeout
    )


class GeocodeForwardResource(SyncAPIResource):
    """
    API прямого геокодинга.

    Примеры на шести языках: https://github.com/atlorium-api/geocoding-api-client
    """

    @cached_property
    def with_raw_response(self) -> GeocodeForwardResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return GeocodeForwardResourceWithRawResponse(self)

    def search(
        self, text: str, *, size: int | None = None, exact_only: bool | None = None, timeout: float | None = None
    ) -> _types.GeocodeForwardResponse:
        """
        Находит координаты по адресу, записанному одной строкой в свободной форме.

        Пример запроса:
        GET /api/geocodeforward?text=Казань, улица Баумана, 13&size=5

        РАЗБОР НОМЕРА ДОМА. Номер отделяется от названия справа налево, по последнему отдельно
        стоящему числу. Поэтому улицы вида «8 Марта 5» и «1905 года 12» разбираются правильно:
        частью названия остаётся то, что ему принадлежит.

        НЕПОЛНОЕ СОВПАДЕНИЕ — ЭТО НЕ ОШИБКА. Если вы прислали «13к2», а в реестре дом заведён
        одной записью «13», вернётся дом 13 с пометкой precision = range. Это осознанно: «найдено
        с оговоркой» полезнее, чем «не найдено». Нужны только буквальные совпадения —
        включите exactOnly.

        КОГДА ИСПОЛЬЗОВАТЬ exactOnly. Там, где приблизительная координата хуже её отсутствия:
        расчёт доставки до подъезда, привязка объекта к конкретному зданию. Включённый режим
        может превратить успешный поиск в «не найдено» — бесплатное, как и любой пустой результат.

        ТАРИФИКАЦИЯ. Запрос не тарифицируется, если адрес не найден, если найденное оказалось
        грубее уровня улицы, если строка некорректна или если геокодер недоступен.

        Аргументы:
            text: Адресная строка в свободной форме. Пример: Казань, улица Баумана, 13
            size: Сколько вариантов вернуть. Значения за пределами допустимого диапазона подтягиваются к границе, а не считаются ошибкой.
            exact_only: Оставить только точные попадания в дом (precision = exact), отбросив всё остальное. По умолчанию выключено.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeForwardResponse",
            self._client.request(_search_options(text=text, size=size, exact_only=exact_only, timeout=timeout)),
        )

    def search_structured(
        self,
        *,
        address: str | None = None,
        locality: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        size: int | None = None,
        exact_only: bool | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeForwardResponse:
        """
        Находит координаты по адресу, разложенному по отдельным полям.

        Пример запроса:
        GET /api/geocodeforward/structured?locality=Казань&address=улица Баумана, 13

        КОГДА ЭТОТ РЕЖИМ ТОЧНЕЕ СВОБОДНОЙ СТРОКИ. Разложенный запрос снимает неопределённость,
        где в строке город, а где улица. Если адрес уже хранится у вас по полям, отправляйте его
        полями: результат устойчивее, особенно для названий, которые встречаются и как улица, и
        как населённый пункт.

        Заполнять все поля не требуется — достаточно тех, что известны. Запрос, в котором не
        заполнено ни одно адресное поле, отклоняется с кодом 400 и не тарифицируется.

        ИНДЕКС РАБОТАЕТ КАК ПРОВЕРКА, А НЕ КАК ФИЛЬТР. Если он задан и не сходится с найденным,
        результаты всё равно возвращаются: индексы в клиентских базах устаревают чаще, чем
        адреса, и отбрасывать из-за этого верный адрес неправильно. Если заполнен ТОЛЬКО
        индекс, запрос равнозначен режиму «что относится к почтовому индексу».

        ТАРИФИКАЦИЯ. Как и в режиме свободной строки: платите только за найденный результат.

        Аргументы:
            address: Улица с номером дома. Пример: улица Баумана, 13
            locality: Населённый пункт. Пример: Казань
            region: Субъект Российской Федерации. Пример: Республика Татарстан
            postal_code: Почтовый индекс. Пример: 420111
            size: Сколько вариантов вернуть.
            exact_only: Оставить только точные попадания в дом. По умолчанию выключено.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeForwardResponse",
            self._client.request(
                _search_structured_options(
                    address=address,
                    locality=locality,
                    region=region,
                    postal_code=postal_code,
                    size=size,
                    exact_only=exact_only,
                    timeout=timeout,
                )
            ),
        )

    def search_batch(
        self,
        queries: Sequence[str],
        *,
        size_per_query: int | None = None,
        exact_only: bool | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeBatchResponse:
        """
        Геокодирует пакет адресов за один запрос. Ответ строго в порядке запроса.

        Пример запроса:
        POST /api/geocodeforward/batch
        {
          "queries": ["Казань, улица Баумана, 13", "Москва, Тверская 1"],
          "sizePerQuery": 1
        }

        ЗАЧЕМ ЭТОТ РЕЖИМ. Типовая задача — прогнать выгрузку из своей системы, десятки тысяч
        строк. Поштучно это столько же обменов по сети, и почти всё время уходит не в поиск, а
        в накладные расходы соединений. Пакет снимает именно их.

        ПОРЯДОК ГАРАНТИРОВАН. Элементов в ответе ровно столько же, сколько строк прислано, и
        идут они в том же порядке. Кроме того, каждый элемент несёт исходную строку в поле
        query — склейка по позиции остаётся возможной, но перестаёт быть единственным способом.

        НЕНАЙДЕННАЯ СТРОКА НЕ ОБРЫВАЕТ ПАКЕТ. У неё будет свой элемент с пустым списком
        matches. Пустая или бессмысленная строка ведёт себя так же.

        ТАРИФИКАЦИЯ. Единиц работы столько, сколько строк РЕАЛЬНО найдено: ненайденная строка
        в пакете бесплатна ровно так же, как поодиночке. Поля requested, found и billedUnits в
        ответе позволяют сверить счёт, не заглядывая в личный кабинет. Пакет, в котором не
        нашлось ничего, не тарифицируется целиком.

        ПРЕДЕЛ. Не больше 1000 адресов за вызов. Пакет большего размера отклоняется целиком
        (400) — лишние строки не отбрасываются молча, иначе вы недосчитались бы результатов,
        не узнав об этом.

        Аргументы:
            queries: Адресные строки в том порядке, в каком их нужно вернуть. Пустые и бессмысленные элементы пакет не обрывают: у них будет свой результат с пустым списком совпадений.
            size_per_query: Сколько вариантов возвращать на каждую строку. По умолчанию один — самый вероятный.
            exact_only: Отдавать только точные попадания в дом. См. exactOnly.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeBatchResponse",
            self._client.request(
                _search_batch_options(
                    queries=queries, size_per_query=size_per_query, exact_only=exact_only, timeout=timeout
                )
            ),
        )

    def get_place(
        self, place_id: str, *, include_boundary: bool | None = None, timeout: float | None = None
    ) -> _types.GeocodePlaceResponse:
        """
        Возвращает карточку объекта по идентификатору из предыдущего ответа геокодинга и, по
        желанию, его административную границу.

        Пример запроса:
        GET /api/geocodeforward/place?placeId=8fd4d1a6-a4a5-4c0d-9c5c-2d0f4b4c1d31

        Пример с границей:
        GET /api/geocodeforward/place?placeId=8fd4d1a6-a4a5-4c0d-9c5c-2d0f4b4c1d31&includeBoundary=true

        ЗАЧЕМ ЭТОТ РЕЖИМ. Идентификатор объекта стабилен НАВСЕГДА: он присвоен государственным
        реестром и не меняется при обновлении наших данных. Сохранив его один раз, вы позже
        получите ТОТ ЖЕ САМЫЙ объект, тогда как повторный поиск по строке может дать другой
        вариант. Отсюда два сценария: обновить координаты ранее сохранённого адреса и подтянуть
        карточку выбранного пользователем варианта, не гоняя поиск заново.

        ГРАНИЦА ЕСТЬ НЕ У ВСЕГО. Она существует у административных образований — субъектов,
        районов, городов. У дома и улицы её нет: запрос не станет ошибкой, поле boundary просто
        останется пустым, и вторая единица работы не спишется. Чтобы получить границу города для
        найденного дома, возьмите идентификатор из поля parentPlaceId.

        ГЕОМЕТРИЯ УПРОЩЕНА. Исходные границы бывают в десятки мегабайт на субъект, и такой ответ
        бесполезен. Точки у самой границы могут попасть не на ту сторону; для точного ответа о
        принадлежности точки используйте обратный геокодинг. Эта оговорка приходит и в самом ответе.

        ТАРИФИКАЦИЯ. Несуществующий идентификатор (404) не тарифицируется.

        Аргументы:
            place_id: Идентификатор объекта — значение поля placeId из любого предыдущего ответа сервисов геокодинга.
            include_boundary: Вернуть также границу объекта в GeoJSON. Стоит дополнительную единицу работы, и только если граница действительно вернулась.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodePlaceResponse",
            self._client.request(
                _get_place_options(place_id=place_id, include_boundary=include_boundary, timeout=timeout)
            ),
        )

    def search_postcode(
        self, code: str, *, size: int | None = None, timeout: float | None = None
    ) -> _types.GeocodePostcodeResponse:
        """
        Возвращает населённый пункт и адресообразующие объекты, которым принадлежит индекс.

        Пример запроса:
        GET /api/geocodeforward/postcode?code=420111

        ЗАЧЕМ ЭТО НУЖНО. Обратная задача к геокодингу и на удивление частая: по индексу из
        платёжки, анкеты или выгрузки понять, какому населённому пункту и каким улицам он
        принадлежит. Типовые применения — автозаполнение формы по введённому индексу и проверка
        того, что индекс в присланных данных не противоречит городу.

        ПОЧЕМУ ОТВЕТ ТОЧНЕЕ ОБЩЕДОСТУПНЫХ СПРАВОЧНИКОВ. Индекс проставлен в государственном
        реестре каждому объекту, то есть приходит из того же источника, что и сам адрес.

        ЧТО НЕ ВОЗВРАЩАЕТСЯ. Дома. На один индекс их десятки тысяч, и такой ответ не отвечает
        на заданный вопрос — спрашивают «где этот индекс», а не «перечисли всё внутри него».

        ТАРИФИКАЦИЯ. У этого режима отдельный, самый низкий тариф: адрес здесь не ищется —
        сервис отвечает, каким объектам принадлежит индекс. Несуществующий индекс (404)
        не тарифицируется.

        Аргументы:
            code: Почтовый индекс — ровно шесть цифр. Пример: 420111
            size: Сколько объектов вернуть.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodePostcodeResponse",
            self._client.request(_search_postcode_options(code=code, size=size, timeout=timeout)),
        )


class AsyncGeocodeForwardResource(AsyncAPIResource):
    """
    API прямого геокодинга.

    Примеры на шести языках: https://github.com/atlorium-api/geocoding-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncGeocodeForwardResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncGeocodeForwardResourceWithRawResponse(self)

    async def search(
        self, text: str, *, size: int | None = None, exact_only: bool | None = None, timeout: float | None = None
    ) -> _types.GeocodeForwardResponse:
        """
        Находит координаты по адресу, записанному одной строкой в свободной форме.

        Пример запроса:
        GET /api/geocodeforward?text=Казань, улица Баумана, 13&size=5

        РАЗБОР НОМЕРА ДОМА. Номер отделяется от названия справа налево, по последнему отдельно
        стоящему числу. Поэтому улицы вида «8 Марта 5» и «1905 года 12» разбираются правильно:
        частью названия остаётся то, что ему принадлежит.

        НЕПОЛНОЕ СОВПАДЕНИЕ — ЭТО НЕ ОШИБКА. Если вы прислали «13к2», а в реестре дом заведён
        одной записью «13», вернётся дом 13 с пометкой precision = range. Это осознанно: «найдено
        с оговоркой» полезнее, чем «не найдено». Нужны только буквальные совпадения —
        включите exactOnly.

        КОГДА ИСПОЛЬЗОВАТЬ exactOnly. Там, где приблизительная координата хуже её отсутствия:
        расчёт доставки до подъезда, привязка объекта к конкретному зданию. Включённый режим
        может превратить успешный поиск в «не найдено» — бесплатное, как и любой пустой результат.

        ТАРИФИКАЦИЯ. Запрос не тарифицируется, если адрес не найден, если найденное оказалось
        грубее уровня улицы, если строка некорректна или если геокодер недоступен.

        Аргументы:
            text: Адресная строка в свободной форме. Пример: Казань, улица Баумана, 13
            size: Сколько вариантов вернуть. Значения за пределами допустимого диапазона подтягиваются к границе, а не считаются ошибкой.
            exact_only: Оставить только точные попадания в дом (precision = exact), отбросив всё остальное. По умолчанию выключено.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeForwardResponse",
            await self._client.request(_search_options(text=text, size=size, exact_only=exact_only, timeout=timeout)),
        )

    async def search_structured(
        self,
        *,
        address: str | None = None,
        locality: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        size: int | None = None,
        exact_only: bool | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeForwardResponse:
        """
        Находит координаты по адресу, разложенному по отдельным полям.

        Пример запроса:
        GET /api/geocodeforward/structured?locality=Казань&address=улица Баумана, 13

        КОГДА ЭТОТ РЕЖИМ ТОЧНЕЕ СВОБОДНОЙ СТРОКИ. Разложенный запрос снимает неопределённость,
        где в строке город, а где улица. Если адрес уже хранится у вас по полям, отправляйте его
        полями: результат устойчивее, особенно для названий, которые встречаются и как улица, и
        как населённый пункт.

        Заполнять все поля не требуется — достаточно тех, что известны. Запрос, в котором не
        заполнено ни одно адресное поле, отклоняется с кодом 400 и не тарифицируется.

        ИНДЕКС РАБОТАЕТ КАК ПРОВЕРКА, А НЕ КАК ФИЛЬТР. Если он задан и не сходится с найденным,
        результаты всё равно возвращаются: индексы в клиентских базах устаревают чаще, чем
        адреса, и отбрасывать из-за этого верный адрес неправильно. Если заполнен ТОЛЬКО
        индекс, запрос равнозначен режиму «что относится к почтовому индексу».

        ТАРИФИКАЦИЯ. Как и в режиме свободной строки: платите только за найденный результат.

        Аргументы:
            address: Улица с номером дома. Пример: улица Баумана, 13
            locality: Населённый пункт. Пример: Казань
            region: Субъект Российской Федерации. Пример: Республика Татарстан
            postal_code: Почтовый индекс. Пример: 420111
            size: Сколько вариантов вернуть.
            exact_only: Оставить только точные попадания в дом. По умолчанию выключено.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeForwardResponse",
            await self._client.request(
                _search_structured_options(
                    address=address,
                    locality=locality,
                    region=region,
                    postal_code=postal_code,
                    size=size,
                    exact_only=exact_only,
                    timeout=timeout,
                )
            ),
        )

    async def search_batch(
        self,
        queries: Sequence[str],
        *,
        size_per_query: int | None = None,
        exact_only: bool | None = None,
        timeout: float | None = None,
    ) -> _types.GeocodeBatchResponse:
        """
        Геокодирует пакет адресов за один запрос. Ответ строго в порядке запроса.

        Пример запроса:
        POST /api/geocodeforward/batch
        {
          "queries": ["Казань, улица Баумана, 13", "Москва, Тверская 1"],
          "sizePerQuery": 1
        }

        ЗАЧЕМ ЭТОТ РЕЖИМ. Типовая задача — прогнать выгрузку из своей системы, десятки тысяч
        строк. Поштучно это столько же обменов по сети, и почти всё время уходит не в поиск, а
        в накладные расходы соединений. Пакет снимает именно их.

        ПОРЯДОК ГАРАНТИРОВАН. Элементов в ответе ровно столько же, сколько строк прислано, и
        идут они в том же порядке. Кроме того, каждый элемент несёт исходную строку в поле
        query — склейка по позиции остаётся возможной, но перестаёт быть единственным способом.

        НЕНАЙДЕННАЯ СТРОКА НЕ ОБРЫВАЕТ ПАКЕТ. У неё будет свой элемент с пустым списком
        matches. Пустая или бессмысленная строка ведёт себя так же.

        ТАРИФИКАЦИЯ. Единиц работы столько, сколько строк РЕАЛЬНО найдено: ненайденная строка
        в пакете бесплатна ровно так же, как поодиночке. Поля requested, found и billedUnits в
        ответе позволяют сверить счёт, не заглядывая в личный кабинет. Пакет, в котором не
        нашлось ничего, не тарифицируется целиком.

        ПРЕДЕЛ. Не больше 1000 адресов за вызов. Пакет большего размера отклоняется целиком
        (400) — лишние строки не отбрасываются молча, иначе вы недосчитались бы результатов,
        не узнав об этом.

        Аргументы:
            queries: Адресные строки в том порядке, в каком их нужно вернуть. Пустые и бессмысленные элементы пакет не обрывают: у них будет свой результат с пустым списком совпадений.
            size_per_query: Сколько вариантов возвращать на каждую строку. По умолчанию один — самый вероятный.
            exact_only: Отдавать только точные попадания в дом. См. exactOnly.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodeBatchResponse",
            await self._client.request(
                _search_batch_options(
                    queries=queries, size_per_query=size_per_query, exact_only=exact_only, timeout=timeout
                )
            ),
        )

    async def get_place(
        self, place_id: str, *, include_boundary: bool | None = None, timeout: float | None = None
    ) -> _types.GeocodePlaceResponse:
        """
        Возвращает карточку объекта по идентификатору из предыдущего ответа геокодинга и, по
        желанию, его административную границу.

        Пример запроса:
        GET /api/geocodeforward/place?placeId=8fd4d1a6-a4a5-4c0d-9c5c-2d0f4b4c1d31

        Пример с границей:
        GET /api/geocodeforward/place?placeId=8fd4d1a6-a4a5-4c0d-9c5c-2d0f4b4c1d31&includeBoundary=true

        ЗАЧЕМ ЭТОТ РЕЖИМ. Идентификатор объекта стабилен НАВСЕГДА: он присвоен государственным
        реестром и не меняется при обновлении наших данных. Сохранив его один раз, вы позже
        получите ТОТ ЖЕ САМЫЙ объект, тогда как повторный поиск по строке может дать другой
        вариант. Отсюда два сценария: обновить координаты ранее сохранённого адреса и подтянуть
        карточку выбранного пользователем варианта, не гоняя поиск заново.

        ГРАНИЦА ЕСТЬ НЕ У ВСЕГО. Она существует у административных образований — субъектов,
        районов, городов. У дома и улицы её нет: запрос не станет ошибкой, поле boundary просто
        останется пустым, и вторая единица работы не спишется. Чтобы получить границу города для
        найденного дома, возьмите идентификатор из поля parentPlaceId.

        ГЕОМЕТРИЯ УПРОЩЕНА. Исходные границы бывают в десятки мегабайт на субъект, и такой ответ
        бесполезен. Точки у самой границы могут попасть не на ту сторону; для точного ответа о
        принадлежности точки используйте обратный геокодинг. Эта оговорка приходит и в самом ответе.

        ТАРИФИКАЦИЯ. Несуществующий идентификатор (404) не тарифицируется.

        Аргументы:
            place_id: Идентификатор объекта — значение поля placeId из любого предыдущего ответа сервисов геокодинга.
            include_boundary: Вернуть также границу объекта в GeoJSON. Стоит дополнительную единицу работы, и только если граница действительно вернулась.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodePlaceResponse",
            await self._client.request(
                _get_place_options(place_id=place_id, include_boundary=include_boundary, timeout=timeout)
            ),
        )

    async def search_postcode(
        self, code: str, *, size: int | None = None, timeout: float | None = None
    ) -> _types.GeocodePostcodeResponse:
        """
        Возвращает населённый пункт и адресообразующие объекты, которым принадлежит индекс.

        Пример запроса:
        GET /api/geocodeforward/postcode?code=420111

        ЗАЧЕМ ЭТО НУЖНО. Обратная задача к геокодингу и на удивление частая: по индексу из
        платёжки, анкеты или выгрузки понять, какому населённому пункту и каким улицам он
        принадлежит. Типовые применения — автозаполнение формы по введённому индексу и проверка
        того, что индекс в присланных данных не противоречит городу.

        ПОЧЕМУ ОТВЕТ ТОЧНЕЕ ОБЩЕДОСТУПНЫХ СПРАВОЧНИКОВ. Индекс проставлен в государственном
        реестре каждому объекту, то есть приходит из того же источника, что и сам адрес.

        ЧТО НЕ ВОЗВРАЩАЕТСЯ. Дома. На один индекс их десятки тысяч, и такой ответ не отвечает
        на заданный вопрос — спрашивают «где этот индекс», а не «перечисли всё внутри него».

        ТАРИФИКАЦИЯ. У этого режима отдельный, самый низкий тариф: адрес здесь не ищется —
        сервис отвечает, каким объектам принадлежит индекс. Несуществующий индекс (404)
        не тарифицируется.

        Аргументы:
            code: Почтовый индекс — ровно шесть цифр. Пример: 420111
            size: Сколько объектов вернуть.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.GeocodePostcodeResponse",
            await self._client.request(_search_postcode_options(code=code, size=size, timeout=timeout)),
        )


class GeocodeForwardResourceWithRawResponse:
    """Методы :class:`GeocodeForwardResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: GeocodeForwardResource) -> None:
        self.search = to_raw_response_wrapper(resource.search)
        self.search_structured = to_raw_response_wrapper(resource.search_structured)
        self.search_batch = to_raw_response_wrapper(resource.search_batch)
        self.get_place = to_raw_response_wrapper(resource.get_place)
        self.search_postcode = to_raw_response_wrapper(resource.search_postcode)


class AsyncGeocodeForwardResourceWithRawResponse:
    """Методы :class:`AsyncGeocodeForwardResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncGeocodeForwardResource) -> None:
        self.search = to_async_raw_response_wrapper(resource.search)
        self.search_structured = to_async_raw_response_wrapper(resource.search_structured)
        self.search_batch = to_async_raw_response_wrapper(resource.search_batch)
        self.get_place = to_async_raw_response_wrapper(resource.get_place)
        self.search_postcode = to_async_raw_response_wrapper(resource.search_postcode)
