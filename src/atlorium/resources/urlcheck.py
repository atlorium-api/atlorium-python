"""
Ресурс «API проверки ссылки»: ``client.urlcheck``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, ensure_sequence
from .._resource import AsyncAPIResource, SyncAPIResource
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import urlcheck as _types

__all__ = ["AsyncUrlCheckResource", "UrlCheckResource"]


def _check_options(*, url: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/urlcheck", params={"url": url}, timeout=timeout)


def _check_batch_options(*, urls: Sequence[str], timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="POST", path="/api/urlcheck/batch", json=ensure_sequence(urls), has_body=True, timeout=timeout
    )


class UrlCheckResource(SyncAPIResource):
    """
    API проверки ссылки.

    Примеры на шести языках: https://github.com/atlorium-api/url-reputation-api-client
    """

    @cached_property
    def with_raw_response(self) -> UrlCheckResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return UrlCheckResourceWithRawResponse(self)

    def check(self, url: str, *, timeout: float | None = None) -> _types.UrlThreatResult:
        """
        Проверяет одну ссылку и возвращает вердикт репутационной проверки.

        Пример запроса:
        GET /api/urlcheck?url=https://example.com/page

        Пример ответа «чисто»:
        { "url": "https://example.com/page", "verdict": "clean", "threatTypes": [],
          "checkedAtUtc": "2026-09-01T10:15:00Z" }

        Пример ответа «угроза»:
        { "url": "http://danger.example/login", "verdict": "threat",
          "threatTypes": ["social_engineering"], "checkedAtUtc": "2026-09-01T10:15:00Z" }

        В демо-режиме (публичный демо-ключ) ветку ответа задаёт домен: адрес на
        malware.example.com вернёт вредонос, на phishing.example.com — фишинг, на
        danger.example.com — сразу две категории, любой другой — «чисто».

        Аргументы:
            url: Проверяемый адрес. Схему можно опустить: «example.com/page» будет приведено к «http://example.com/page». Принимаются только адреса со схемой http или https. В ответе адрес возвращается в приведённом виде — именно в нём он и проверялся.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.UrlThreatResult", self._client.request(_check_options(url=url, timeout=timeout)))

    def check_batch(self, urls: Sequence[str], *, timeout: float | None = None) -> _types.UrlThreatBatchResponse:
        """
        Проверяет пакет ссылок за один вызов (до 100 адресов).

        Порядок результатов совпадает с порядком присланных ссылок — сопоставляйте по индексу.

        Пример запроса:
        POST /api/urlcheck/batch
        [ "https://example.com", "http://phishing.example.com/login" ]

        ТАРИФИКАЦИЯ ПАКЕТА. Списывается по числу ссылок с НАСТОЯЩИМ вердиктом. Если по трём
        строкам из ста вердикт получить не удалось, спишется девяносто семь единиц, а не сто.

        Аргументы:
            urls: Список проверяемых адресов. Пустые строки и повторы отбрасываются до проверки: повтор не добавляет работы и оплачиваться не должен. Максимум — 100 адресов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.UrlThreatBatchResponse", self._client.request(_check_batch_options(urls=urls, timeout=timeout))
        )


class AsyncUrlCheckResource(AsyncAPIResource):
    """
    API проверки ссылки.

    Примеры на шести языках: https://github.com/atlorium-api/url-reputation-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncUrlCheckResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncUrlCheckResourceWithRawResponse(self)

    async def check(self, url: str, *, timeout: float | None = None) -> _types.UrlThreatResult:
        """
        Проверяет одну ссылку и возвращает вердикт репутационной проверки.

        Пример запроса:
        GET /api/urlcheck?url=https://example.com/page

        Пример ответа «чисто»:
        { "url": "https://example.com/page", "verdict": "clean", "threatTypes": [],
          "checkedAtUtc": "2026-09-01T10:15:00Z" }

        Пример ответа «угроза»:
        { "url": "http://danger.example/login", "verdict": "threat",
          "threatTypes": ["social_engineering"], "checkedAtUtc": "2026-09-01T10:15:00Z" }

        В демо-режиме (публичный демо-ключ) ветку ответа задаёт домен: адрес на
        malware.example.com вернёт вредонос, на phishing.example.com — фишинг, на
        danger.example.com — сразу две категории, любой другой — «чисто».

        Аргументы:
            url: Проверяемый адрес. Схему можно опустить: «example.com/page» будет приведено к «http://example.com/page». Принимаются только адреса со схемой http или https. В ответе адрес возвращается в приведённом виде — именно в нём он и проверялся.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("_types.UrlThreatResult", await self._client.request(_check_options(url=url, timeout=timeout)))

    async def check_batch(self, urls: Sequence[str], *, timeout: float | None = None) -> _types.UrlThreatBatchResponse:
        """
        Проверяет пакет ссылок за один вызов (до 100 адресов).

        Порядок результатов совпадает с порядком присланных ссылок — сопоставляйте по индексу.

        Пример запроса:
        POST /api/urlcheck/batch
        [ "https://example.com", "http://phishing.example.com/login" ]

        ТАРИФИКАЦИЯ ПАКЕТА. Списывается по числу ссылок с НАСТОЯЩИМ вердиктом. Если по трём
        строкам из ста вердикт получить не удалось, спишется девяносто семь единиц, а не сто.

        Аргументы:
            urls: Список проверяемых адресов. Пустые строки и повторы отбрасываются до проверки: повтор не добавляет работы и оплачиваться не должен. Максимум — 100 адресов.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.UrlThreatBatchResponse",
            await self._client.request(_check_batch_options(urls=urls, timeout=timeout)),
        )


class UrlCheckResourceWithRawResponse:
    """Методы :class:`UrlCheckResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: UrlCheckResource) -> None:
        self.check = to_raw_response_wrapper(resource.check)
        self.check_batch = to_raw_response_wrapper(resource.check_batch)


class AsyncUrlCheckResourceWithRawResponse:
    """Методы :class:`AsyncUrlCheckResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncUrlCheckResource) -> None:
        self.check = to_async_raw_response_wrapper(resource.check)
        self.check_batch = to_async_raw_response_wrapper(resource.check_batch)
