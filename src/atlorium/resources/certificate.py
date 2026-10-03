"""
Ресурс «API проверки SSL-сертификата»: ``client.certificate``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import certificate as _types

__all__ = ["AsyncCertificateResource", "CertificateResource"]


def _check_options(*, host: str, port: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/certificate", params={"host": host, "port": port}, timeout=timeout)


def _check_url_options(*, url: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/certificate/url", params={"url": url}, timeout=timeout)


def _check_batch_options(*, hosts: str | Sequence[str], port: int | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/certificate/batch",
        params={"hosts": ensure_sequence(hosts), "port": port},
        timeout=timeout,
    )


class CertificateResource(SyncAPIResource):
    """
    API проверки SSL-сертификата.

    Примеры на шести языках: https://github.com/atlorium-api/ssl-certificate-check-api-client
    """

    @cached_property
    def with_raw_response(self) -> CertificateResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return CertificateResourceWithRawResponse(self)

    def check(self, host: str, *, port: int | None = None, timeout: float | None = None) -> _types.CertificateData:
        """
        Проверяет SSL/TLS сертификат по доменному имени и порту.
        Подключается к серверу, извлекает сертификат и возвращает подробную информацию о нём.

        Пример запроса:
        GET /api/certificate?host=google.com
        GET /api/certificate?host=mail.server.com&port=993

        Сервис устанавливает TLS-соединение с указанным хостом и портом,
        извлекает представленный сервером сертификат и анализирует его содержимое.

        Аргументы:
            host: Доменное имя сервера для проверки.  Поддерживаемые форматы: - Чистое доменное имя: example.com - С поддоменом: www.example.com - IP-адрес: 192.168.1.1  Примеры: google.com, github.com, microsoft.com
            port: Порт для подключения (необязательный, по умолчанию 443).  Стандартные порты: - 443: HTTPS (по умолчанию) - 8443: Альтернативный HTTPS - 993: IMAPS (почта) - 995: POP3S (почта) - 465: SMTPS (отправка почты)  Допустимый диапазон: от 1 до 65535
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CertificateData", self._client.request(_check_options(host=host, port=port, timeout=timeout))
        )

    def check_url(self, url: str, *, timeout: float | None = None) -> _types.CertificateData:
        """
        Проверяет SSL/TLS сертификат по полному URL.
        Автоматически извлекает хост и порт из URL и выполняет проверку сертификата.

        Пример запроса:
        GET /api/certificate/url?url=https://google.com
        GET /api/certificate/url?url=https://mail.server.com:993

        Этот метод удобен, когда вы хотите проверить сертификат по URL,
        который пользователь скопировал из браузера — без необходимости
        разбирать URL на хост и порт вручную.

        Аргументы:
            url: Полный URL для проверки.  Поддерживаемые форматы: - Полный URL с протоколом: https://example.com - URL с портом: https://example.com:8443 - URL с путём: https://example.com:8443/api/v1  Примеры: - https://google.com - https://secure.bank.com:8443 - https://api.github.com/users  Если порт не указан, используется стандартный порт 443.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CertificateData", self._client.request(_check_url_options(url=url, timeout=timeout)))

    def check_batch(
        self, hosts: str | Sequence[str], *, port: int | None = None, timeout: float | None = None
    ) -> list[_types.CertificateData]:
        """
        Проверяет несколько SSL/TLS сертификатов одновременно (пакетная проверка).
        Позволяет проверить до 10 хостов за один запрос параллельно.

        Пример запроса:
        GET /api/certificate/batch?hosts=google.com,github.com,microsoft.com
        GET /api/certificate/batch?hosts=mail1.com,mail2.com&port=993

        Все проверки выполняются параллельно для быстрого получения результатов.
        Если один из сертификатов недоступен, вся операция может завершиться ошибкой.

        Аргументы:
            hosts: Список доменных имён через запятую.  Формат: host1,host2,host3  Ограничения: - Минимум 1 хост - Максимум 10 хостов за один запрос - Пробелы вокруг запятых игнорируются - Повторы одного и того же хоста схлопываются (за одну проверку платите один раз)  ТАРИФИКАЦИЯ: похостная. Каждый хост — отдельная проверка сертификата, поэтому пакет из N хостов стоит столько же, сколько N одиночных проверок, и на столько же уменьшает дневной бесплатный лимит. Оплачиваются хосты, по которым получен вердикт (недоступный сервер — тоже вердикт); при сбое всего запроса не списывается ничего.  Примеры: - google.com,github.com,microsoft.com - google.com, github.com, microsoft.com (с пробелами — допустимо)
            port: Порт для подключения ко ВСЕМ хостам (необязательный, по умолчанию 443).  Важно: один порт применяется ко всем хостам в списке. Если нужны разные порты, выполните отдельные запросы.  Допустимый диапазон: от 1 до 65535
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "list[_types.CertificateData]",
            self._client.request(_check_batch_options(hosts=hosts, port=port, timeout=timeout)),
        )


class AsyncCertificateResource(AsyncAPIResource):
    """
    API проверки SSL-сертификата.

    Примеры на шести языках: https://github.com/atlorium-api/ssl-certificate-check-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncCertificateResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncCertificateResourceWithRawResponse(self)

    async def check(
        self, host: str, *, port: int | None = None, timeout: float | None = None
    ) -> _types.CertificateData:
        """
        Проверяет SSL/TLS сертификат по доменному имени и порту.
        Подключается к серверу, извлекает сертификат и возвращает подробную информацию о нём.

        Пример запроса:
        GET /api/certificate?host=google.com
        GET /api/certificate?host=mail.server.com&port=993

        Сервис устанавливает TLS-соединение с указанным хостом и портом,
        извлекает представленный сервером сертификат и анализирует его содержимое.

        Аргументы:
            host: Доменное имя сервера для проверки.  Поддерживаемые форматы: - Чистое доменное имя: example.com - С поддоменом: www.example.com - IP-адрес: 192.168.1.1  Примеры: google.com, github.com, microsoft.com
            port: Порт для подключения (необязательный, по умолчанию 443).  Стандартные порты: - 443: HTTPS (по умолчанию) - 8443: Альтернативный HTTPS - 993: IMAPS (почта) - 995: POP3S (почта) - 465: SMTPS (отправка почты)  Допустимый диапазон: от 1 до 65535
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CertificateData", await self._client.request(_check_options(host=host, port=port, timeout=timeout))
        )

    async def check_url(self, url: str, *, timeout: float | None = None) -> _types.CertificateData:
        """
        Проверяет SSL/TLS сертификат по полному URL.
        Автоматически извлекает хост и порт из URL и выполняет проверку сертификата.

        Пример запроса:
        GET /api/certificate/url?url=https://google.com
        GET /api/certificate/url?url=https://mail.server.com:993

        Этот метод удобен, когда вы хотите проверить сертификат по URL,
        который пользователь скопировал из браузера — без необходимости
        разбирать URL на хост и порт вручную.

        Аргументы:
            url: Полный URL для проверки.  Поддерживаемые форматы: - Полный URL с протоколом: https://example.com - URL с портом: https://example.com:8443 - URL с путём: https://example.com:8443/api/v1  Примеры: - https://google.com - https://secure.bank.com:8443 - https://api.github.com/users  Если порт не указан, используется стандартный порт 443.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.CertificateData", await self._client.request(_check_url_options(url=url, timeout=timeout)))

    async def check_batch(
        self, hosts: str | Sequence[str], *, port: int | None = None, timeout: float | None = None
    ) -> list[_types.CertificateData]:
        """
        Проверяет несколько SSL/TLS сертификатов одновременно (пакетная проверка).
        Позволяет проверить до 10 хостов за один запрос параллельно.

        Пример запроса:
        GET /api/certificate/batch?hosts=google.com,github.com,microsoft.com
        GET /api/certificate/batch?hosts=mail1.com,mail2.com&port=993

        Все проверки выполняются параллельно для быстрого получения результатов.
        Если один из сертификатов недоступен, вся операция может завершиться ошибкой.

        Аргументы:
            hosts: Список доменных имён через запятую.  Формат: host1,host2,host3  Ограничения: - Минимум 1 хост - Максимум 10 хостов за один запрос - Пробелы вокруг запятых игнорируются - Повторы одного и того же хоста схлопываются (за одну проверку платите один раз)  ТАРИФИКАЦИЯ: похостная. Каждый хост — отдельная проверка сертификата, поэтому пакет из N хостов стоит столько же, сколько N одиночных проверок, и на столько же уменьшает дневной бесплатный лимит. Оплачиваются хосты, по которым получен вердикт (недоступный сервер — тоже вердикт); при сбое всего запроса не списывается ничего.  Примеры: - google.com,github.com,microsoft.com - google.com, github.com, microsoft.com (с пробелами — допустимо)
            port: Порт для подключения ко ВСЕМ хостам (необязательный, по умолчанию 443).  Важно: один порт применяется ко всем хостам в списке. Если нужны разные порты, выполните отдельные запросы.  Допустимый диапазон: от 1 до 65535
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "list[_types.CertificateData]",
            await self._client.request(_check_batch_options(hosts=hosts, port=port, timeout=timeout)),
        )


class CertificateResourceWithRawResponse:
    """Методы :class:`CertificateResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: CertificateResource) -> None:
        self.check = to_raw_response_wrapper(resource.check)
        self.check_url = to_raw_response_wrapper(resource.check_url)
        self.check_batch = to_raw_response_wrapper(resource.check_batch)


class AsyncCertificateResourceWithRawResponse:
    """Методы :class:`AsyncCertificateResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncCertificateResource) -> None:
        self.check = to_async_raw_response_wrapper(resource.check)
        self.check_url = to_async_raw_response_wrapper(resource.check_url)
        self.check_batch = to_async_raw_response_wrapper(resource.check_batch)
