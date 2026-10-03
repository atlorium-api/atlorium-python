"""
Ресурс «API аудита сайта»: ``client.pagespeed``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import pagespeed as _types

__all__ = ["AsyncPageSpeedResource", "PageSpeedResource"]


def _audit_options(
    *, url: str, strategy: _types.SiteStrategy | None, force_refresh: bool | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/pagespeed",
        params={"url": url, "strategy": strategy, "forceRefresh": force_refresh},
        timeout=timeout,
        default_timeout=120,
    )


def _audit_batch_options(
    *, strategy: _types.SiteStrategy | None, urls: Sequence[str], timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/pagespeed/batch",
        params={"strategy": strategy},
        json=ensure_sequence(urls),
        has_body=True,
        timeout=timeout,
        default_timeout=600,
    )


class PageSpeedResource(SyncAPIResource):
    """
    API аудита сайта.

    Примеры на шести языках: https://github.com/atlorium-api/core-web-vitals-api-client
    """

    @cached_property
    def with_raw_response(self) -> PageSpeedResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return PageSpeedResourceWithRawResponse(self)

    def audit(
        self,
        url: str,
        *,
        strategy: _types.SiteStrategy | None = None,
        force_refresh: bool | None = None,
        timeout: float | None = None,
    ) -> _types.SitePerformanceReport:
        """
        Выполняет аудит одной страницы и возвращает полный отчёт.

        Примеры запросов:
        GET /api/pagespeed?url=https://example.com
        GET /api/pagespeed?url=https://example.com&strategy=desktop
        GET /api/pagespeed?url=https://example.com&forceRefresh=true

        ⚠ Ответ занимает 10–30 секунд: страница действительно загружается в браузере.

        КАК ЧИТАТЬ ОТЧЁТ. Начните с поля message — это одна фраза с выводом. Затем сверьте
        finalUrl с запрошенным адресом: если они различаются, вас увела переадресация и
        измерялась другая страница (частый случай — редирект на страницу согласия с cookie).
        Дальше — performanceScore как быстрый ориентир и opportunities сверху вниз: первые
        два-три пункта и есть то, чем стоит заняться.

        ЧТО ЗНАЧИТ «ЭКОНОМИЯ» В РЕКОМЕНДАЦИЯХ. Это оценка, а не обещание: столько
        миллисекунд отыграется, если пункт выполнить полностью. Пункты пересекаются между
        собой, поэтому складывать экономию по всему списку и ждать такой суммы не следует.

        Аргументы:
            url: Адрес страницы. Схему можно опустить: «example.com» будет приведено к «https://example.com/». Принимаются только адреса со схемой http или https. Страница должна открываться публично — без авторизации и без блокировки автоматических обращений.
            strategy: Профиль устройства: mobile (по умолчанию) или desktop. Влияет на результат сильно — сравнивать между собой можно только замеры на одном профиле.
            force_refresh: true — выполнить прогон заново, минуя сохранённый результат. Нужен ровно в одном сценарии, зато в самом частом: «я только что выкатил оптимизацию — стало быстрее?». Сохранённый отчёт в этот момент показал бы состояние ДО правки. Тарифицируется как обычный запрос: работа выполняется полностью.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SitePerformanceReport",
            self._client.request(
                _audit_options(url=url, strategy=strategy, force_refresh=force_refresh, timeout=timeout)
            ),
        )

    def audit_batch(
        self, urls: Sequence[str], *, strategy: _types.SiteStrategy | None = None, timeout: float | None = None
    ) -> _types.SitePerformanceBatchResponse:
        """
        Выполняет аудит пакета адресов за один вызов (до 20 адресов).

        Порядок результатов совпадает с порядком присланных адресов — сопоставляйте по индексу.

        ⚠ ПАКЕТ ИДЁТ МИНУТАМИ. Двадцать адресов — примерно две минуты: адреса обрабатываются
        по четыре одновременно, каждый прогон 10–30 секунд. Поставьте таймаут своего клиента
        с запасом или разбейте работу на пакеты поменьше — в деньгах вы ничего не потеряете,
        единица стоит столько же.

        Пример запроса:
        POST /api/pagespeed/batch?strategy=mobile
        [ "https://example.com", "https://example.com/catalog" ]

        ТАРИФИКАЦИЯ ПАКЕТА. Списывается по числу адресов, по которым аудит РЕАЛЬНО состоялся.
        Если из двадцати страниц три не открылись, спишется семнадцать единиц, а не двадцать.
        Принудительного обновления в обход сохранённых отчётов у пакетного режима нет: пакет —
        это регулярный обход списка страниц, и в нём ценно как раз то, что уже посчитанное
        берётся готовым.

        Аргументы:
            strategy: Профиль устройства, единый для всего пакета.
            urls: Список адресов страниц. Пустые строки и повторы отбрасываются до аудита: повтор не добавляет работы и оплачиваться не должен. Максимум — 20 адресов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SitePerformanceBatchResponse",
            self._client.request(_audit_batch_options(strategy=strategy, urls=urls, timeout=timeout)),
        )


class AsyncPageSpeedResource(AsyncAPIResource):
    """
    API аудита сайта.

    Примеры на шести языках: https://github.com/atlorium-api/core-web-vitals-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncPageSpeedResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncPageSpeedResourceWithRawResponse(self)

    async def audit(
        self,
        url: str,
        *,
        strategy: _types.SiteStrategy | None = None,
        force_refresh: bool | None = None,
        timeout: float | None = None,
    ) -> _types.SitePerformanceReport:
        """
        Выполняет аудит одной страницы и возвращает полный отчёт.

        Примеры запросов:
        GET /api/pagespeed?url=https://example.com
        GET /api/pagespeed?url=https://example.com&strategy=desktop
        GET /api/pagespeed?url=https://example.com&forceRefresh=true

        ⚠ Ответ занимает 10–30 секунд: страница действительно загружается в браузере.

        КАК ЧИТАТЬ ОТЧЁТ. Начните с поля message — это одна фраза с выводом. Затем сверьте
        finalUrl с запрошенным адресом: если они различаются, вас увела переадресация и
        измерялась другая страница (частый случай — редирект на страницу согласия с cookie).
        Дальше — performanceScore как быстрый ориентир и opportunities сверху вниз: первые
        два-три пункта и есть то, чем стоит заняться.

        ЧТО ЗНАЧИТ «ЭКОНОМИЯ» В РЕКОМЕНДАЦИЯХ. Это оценка, а не обещание: столько
        миллисекунд отыграется, если пункт выполнить полностью. Пункты пересекаются между
        собой, поэтому складывать экономию по всему списку и ждать такой суммы не следует.

        Аргументы:
            url: Адрес страницы. Схему можно опустить: «example.com» будет приведено к «https://example.com/». Принимаются только адреса со схемой http или https. Страница должна открываться публично — без авторизации и без блокировки автоматических обращений.
            strategy: Профиль устройства: mobile (по умолчанию) или desktop. Влияет на результат сильно — сравнивать между собой можно только замеры на одном профиле.
            force_refresh: true — выполнить прогон заново, минуя сохранённый результат. Нужен ровно в одном сценарии, зато в самом частом: «я только что выкатил оптимизацию — стало быстрее?». Сохранённый отчёт в этот момент показал бы состояние ДО правки. Тарифицируется как обычный запрос: работа выполняется полностью.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SitePerformanceReport",
            await self._client.request(
                _audit_options(url=url, strategy=strategy, force_refresh=force_refresh, timeout=timeout)
            ),
        )

    async def audit_batch(
        self, urls: Sequence[str], *, strategy: _types.SiteStrategy | None = None, timeout: float | None = None
    ) -> _types.SitePerformanceBatchResponse:
        """
        Выполняет аудит пакета адресов за один вызов (до 20 адресов).

        Порядок результатов совпадает с порядком присланных адресов — сопоставляйте по индексу.

        ⚠ ПАКЕТ ИДЁТ МИНУТАМИ. Двадцать адресов — примерно две минуты: адреса обрабатываются
        по четыре одновременно, каждый прогон 10–30 секунд. Поставьте таймаут своего клиента
        с запасом или разбейте работу на пакеты поменьше — в деньгах вы ничего не потеряете,
        единица стоит столько же.

        Пример запроса:
        POST /api/pagespeed/batch?strategy=mobile
        [ "https://example.com", "https://example.com/catalog" ]

        ТАРИФИКАЦИЯ ПАКЕТА. Списывается по числу адресов, по которым аудит РЕАЛЬНО состоялся.
        Если из двадцати страниц три не открылись, спишется семнадцать единиц, а не двадцать.
        Принудительного обновления в обход сохранённых отчётов у пакетного режима нет: пакет —
        это регулярный обход списка страниц, и в нём ценно как раз то, что уже посчитанное
        берётся готовым.

        Аргументы:
            strategy: Профиль устройства, единый для всего пакета.
            urls: Список адресов страниц. Пустые строки и повторы отбрасываются до аудита: повтор не добавляет работы и оплачиваться не должен. Максимум — 20 адресов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.SitePerformanceBatchResponse",
            await self._client.request(_audit_batch_options(strategy=strategy, urls=urls, timeout=timeout)),
        )


class PageSpeedResourceWithRawResponse:
    """Методы :class:`PageSpeedResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: PageSpeedResource) -> None:
        self.audit = to_raw_response_wrapper(resource.audit)
        self.audit_batch = to_raw_response_wrapper(resource.audit_batch)


class AsyncPageSpeedResourceWithRawResponse:
    """Методы :class:`AsyncPageSpeedResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncPageSpeedResource) -> None:
        self.audit = to_async_raw_response_wrapper(resource.audit)
        self.audit_batch = to_async_raw_response_wrapper(resource.audit_batch)
