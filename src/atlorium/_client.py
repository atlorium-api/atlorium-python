"""
Клиенты Atlorium: синхронный :class:`Atlorium` и асинхронный :class:`AsyncAtlorium`.

    from atlorium import Atlorium

    client = Atlorium()  # без ключа — публичный демо-ключ, ответы-моки
    card = client.egrul.get("7707083893")

Ресурсы (``client.egrul``, ``client.cbr`` и т.д.) подключаются из сгенерированного модуля
``_resources_mixin.py`` — см. ``scripts/generate.py``.
"""

from __future__ import annotations

from types import TracebackType

import httpx

from ._base_client import AsyncAPIClient, SyncAPIClient
from ._resources_mixin import AsyncResourcesMixin, SyncResourcesMixin

__all__ = ["AsyncAtlorium", "Atlorium"]


class Atlorium(SyncResourcesMixin, SyncAPIClient):
    """Синхронный клиент API Atlorium.

    Аргументы:
        api_key: API-ключ. Если не задан — переменная окружения ``ATLORIUM_API_KEY``,
            а если нет и её — публичный демо-ключ ``ak_sandbox_demo_mockdata_v1``
            (ответы-моки, детерминированные; см. :attr:`is_sandbox`).
        base_url: адрес API, по умолчанию ``https://atlorium.com`` или ``ATLORIUM_BASE_URL``.
        timeout: таймаут одного HTTP-запроса в секундах, по умолчанию 30. Для ``aichat.send``
            действует не меньше 660 с. Любой метод принимает собственный ``timeout``.
        max_retries: сколько раз повторять запрос на 429, 503 и сетевых ошибках, по умолчанию 2
            (503 при плановых работах не повторяется).
        http_client: свой ``httpx.Client`` (прокси, транспорт для тестов и т.п.).
            Такой клиент SDK не закрывает — его жизненным циклом управляет вызывающий код.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

    def with_options(self, *, timeout: float | None = None, max_retries: int | None = None) -> Atlorium:
        """Копия клиента с другими таймаутом и/или числом ретраев. Соединения общие."""
        copy = Atlorium(
            api_key=self._api_key,
            base_url=self.base_url,
            timeout=self.timeout if timeout is None else timeout,
            max_retries=self.max_retries if max_retries is None else max_retries,
            http_client=self._http,
        )
        copy._owns_http_client = False
        copy._sleep = self._sleep
        return copy

    def __enter__(self) -> Atlorium:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class AsyncAtlorium(AsyncResourcesMixin, AsyncAPIClient):
    """Асинхронный клиент API Atlorium. Аргументы — как у :class:`Atlorium`,
    но ``http_client`` — это ``httpx.AsyncClient``.

        async with AsyncAtlorium() as client:
            card = await client.egrul.get("7707083893")
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

    def with_options(self, *, timeout: float | None = None, max_retries: int | None = None) -> AsyncAtlorium:
        """Копия клиента с другими таймаутом и/или числом ретраев. Соединения общие."""
        copy = AsyncAtlorium(
            api_key=self._api_key,
            base_url=self.base_url,
            timeout=self.timeout if timeout is None else timeout,
            max_retries=self.max_retries if max_retries is None else max_retries,
            http_client=self._http,
        )
        copy._owns_http_client = False
        copy._sleep = self._sleep
        return copy

    async def __aenter__(self) -> AsyncAtlorium:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
