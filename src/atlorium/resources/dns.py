"""
Ресурс «API проверки DNS»: ``client.dns``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import dns as _types

__all__ = ["AsyncDnsResource", "DnsResource"]


def _lookup_options(*, domain: str, resolver: str | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET", path="/api/dns/lookup", params={"domain": domain, "resolver": resolver}, timeout=timeout
    )


def _check_propagation_options(
    *, domain: str, resolvers: str | Sequence[str] | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/dns/propagation",
        params={"domain": domain, "resolvers": None if resolvers is None else ensure_sequence(resolvers)},
        timeout=timeout,
    )


class DnsResource(SyncAPIResource):
    """
    API проверки DNS.

    Примеры на шести языках: https://github.com/atlorium-api/dns-lookup-api-client
    """

    @cached_property
    def with_raw_response(self) -> DnsResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return DnsResourceWithRawResponse(self)

    def lookup(
        self, domain: str, *, resolver: str | None = None, timeout: float | None = None
    ) -> _types.DnsLookupResponse:
        """
        Выполняет DNS-запрос для основных типов записей (A, AAAA, MX, TXT, CNAME, NS).
        Возвращает все найденные записи для указанного домена.

        Пример запроса:
        GET /api/dns/lookup?domain=google.com
        GET /api/dns/lookup?domain=microsoft.com&resolver=8.8.8.8

        Пример ответа:
        {
          "domain": "google.com",
          "resolver": "1.1.1.1",
          "records": {
            "A": ["142.250.185.78"],
            "AAAA": ["2a00:1450:4010:c08::64"],
            "MX": ["smtp.google.com"],
            "NS": ["ns1.google.com", "ns2.google.com"]
          }
        }

        Аргументы:
            domain: Доменное имя для запроса.  Формат: чистое доменное имя без протокола.  Примеры: - example.com - sub.example.com - google.com  Не допускаются: - URL с протоколом (https://example.com) - IP-адреса
            resolver: IP-адрес DNS-резолвера для выполнения запроса (необязательный).  По умолчанию: Cloudflare (1.1.1.1)  Примеры альтернативных резолверов: - 8.8.8.8 (Google) - 208.67.222.222 (OpenDNS) - 9.9.9.9 (Quad9) - Корпоративный DNS-сервер
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.DnsLookupResponse",
            self._client.request(_lookup_options(domain=domain, resolver=resolver, timeout=timeout)),
        )

    def check_propagation(
        self, domain: str, *, resolvers: str | Sequence[str] | None = None, timeout: float | None = None
    ) -> _types.DnsPropagationResponse:
        """
        Проверяет распространение DNS-записей (пропагацию) через несколько публичных резолверов.
        Полезно для проверки того, обновились ли DNS-записи на всех серверах после изменения.

        Пример запроса:
        GET /api/dns/propagation?domain=example.com
        GET /api/dns/propagation?domain=new-site.com&resolvers=8.8.8.8,1.1.1.1

        Пример использования:
        После изменения DNS-записей домена выполните этот запрос,
        чтобы проверить, распространились ли изменения на все резолверы.
        Полная пропагация может занять от нескольких минут до 48 часов.

        Аргументы:
            domain: Доменное имя для проверки.  Формат: чистое доменное имя без протокола.  Примеры: - example.com - new-domain.com
            resolvers: Список IP-адресов DNS-резолверов через запятую (необязательный).  По умолчанию используются 4 резолвера: - Google (8.8.8.8) - Cloudflare (1.1.1.1) - OpenDNS (208.67.222.222) - Quad9 (9.9.9.9)  Ограничения: - Максимум 8 резолверов за один запрос - Только публичные IP-адреса (внутренние и зарезервированные отклоняются) - Повторы одного и того же адреса схлопываются (за один опрос платите один раз) - Некорректный адрес или превышение лимита — 400 Bad Request (список не обрезается молча)  ТАРИФИКАЦИЯ: порезолверная. Каждый резолвер опрашивается отдельно по всем типам записей, поэтому проверка по N резолверам стоит столько же, сколько N обычных DNS-запросов, и на столько же уменьшает дневной бесплатный лимит. Запрос без этого параметра опрашивает 4 резолвера по умолчанию и тарифицируется как 4 единицы.  Пример: 8.8.8.8,1.1.1.1,208.67.222.222
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.DnsPropagationResponse",
            self._client.request(_check_propagation_options(domain=domain, resolvers=resolvers, timeout=timeout)),
        )


class AsyncDnsResource(AsyncAPIResource):
    """
    API проверки DNS.

    Примеры на шести языках: https://github.com/atlorium-api/dns-lookup-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncDnsResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncDnsResourceWithRawResponse(self)

    async def lookup(
        self, domain: str, *, resolver: str | None = None, timeout: float | None = None
    ) -> _types.DnsLookupResponse:
        """
        Выполняет DNS-запрос для основных типов записей (A, AAAA, MX, TXT, CNAME, NS).
        Возвращает все найденные записи для указанного домена.

        Пример запроса:
        GET /api/dns/lookup?domain=google.com
        GET /api/dns/lookup?domain=microsoft.com&resolver=8.8.8.8

        Пример ответа:
        {
          "domain": "google.com",
          "resolver": "1.1.1.1",
          "records": {
            "A": ["142.250.185.78"],
            "AAAA": ["2a00:1450:4010:c08::64"],
            "MX": ["smtp.google.com"],
            "NS": ["ns1.google.com", "ns2.google.com"]
          }
        }

        Аргументы:
            domain: Доменное имя для запроса.  Формат: чистое доменное имя без протокола.  Примеры: - example.com - sub.example.com - google.com  Не допускаются: - URL с протоколом (https://example.com) - IP-адреса
            resolver: IP-адрес DNS-резолвера для выполнения запроса (необязательный).  По умолчанию: Cloudflare (1.1.1.1)  Примеры альтернативных резолверов: - 8.8.8.8 (Google) - 208.67.222.222 (OpenDNS) - 9.9.9.9 (Quad9) - Корпоративный DNS-сервер
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.DnsLookupResponse",
            await self._client.request(_lookup_options(domain=domain, resolver=resolver, timeout=timeout)),
        )

    async def check_propagation(
        self, domain: str, *, resolvers: str | Sequence[str] | None = None, timeout: float | None = None
    ) -> _types.DnsPropagationResponse:
        """
        Проверяет распространение DNS-записей (пропагацию) через несколько публичных резолверов.
        Полезно для проверки того, обновились ли DNS-записи на всех серверах после изменения.

        Пример запроса:
        GET /api/dns/propagation?domain=example.com
        GET /api/dns/propagation?domain=new-site.com&resolvers=8.8.8.8,1.1.1.1

        Пример использования:
        После изменения DNS-записей домена выполните этот запрос,
        чтобы проверить, распространились ли изменения на все резолверы.
        Полная пропагация может занять от нескольких минут до 48 часов.

        Аргументы:
            domain: Доменное имя для проверки.  Формат: чистое доменное имя без протокола.  Примеры: - example.com - new-domain.com
            resolvers: Список IP-адресов DNS-резолверов через запятую (необязательный).  По умолчанию используются 4 резолвера: - Google (8.8.8.8) - Cloudflare (1.1.1.1) - OpenDNS (208.67.222.222) - Quad9 (9.9.9.9)  Ограничения: - Максимум 8 резолверов за один запрос - Только публичные IP-адреса (внутренние и зарезервированные отклоняются) - Повторы одного и того же адреса схлопываются (за один опрос платите один раз) - Некорректный адрес или превышение лимита — 400 Bad Request (список не обрезается молча)  ТАРИФИКАЦИЯ: порезолверная. Каждый резолвер опрашивается отдельно по всем типам записей, поэтому проверка по N резолверам стоит столько же, сколько N обычных DNS-запросов, и на столько же уменьшает дневной бесплатный лимит. Запрос без этого параметра опрашивает 4 резолвера по умолчанию и тарифицируется как 4 единицы.  Пример: 8.8.8.8,1.1.1.1,208.67.222.222
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.DnsPropagationResponse",
            await self._client.request(_check_propagation_options(domain=domain, resolvers=resolvers, timeout=timeout)),
        )


class DnsResourceWithRawResponse:
    """Методы :class:`DnsResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: DnsResource) -> None:
        self.lookup = to_raw_response_wrapper(resource.lookup)
        self.check_propagation = to_raw_response_wrapper(resource.check_propagation)


class AsyncDnsResourceWithRawResponse:
    """Методы :class:`AsyncDnsResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncDnsResource) -> None:
        self.lookup = to_async_raw_response_wrapper(resource.lookup)
        self.check_propagation = to_async_raw_response_wrapper(resource.check_propagation)
