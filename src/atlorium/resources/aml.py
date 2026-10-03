"""
Ресурс «API AML-скоринга»: ``client.aml``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import aml as _types

__all__ = ["AmlResource", "AsyncAmlResource"]


def _screen_options(*, wallet_address: str, blockchain: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/aml/screen",
        json=strip_none({"walletAddress": wallet_address, "blockchain": blockchain}),
        has_body=True,
        timeout=timeout,
    )


def _validate_options(*, wallet_address: str, blockchain: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="GET",
        path="/api/aml/validate",
        params={"walletAddress": wallet_address, "blockchain": blockchain},
        timeout=timeout,
    )


class AmlResource(SyncAPIResource):
    """
    API AML-скоринга.

    Примеры на шести языках: https://github.com/atlorium-api/aml-crypto-screening-api-client
    """

    @cached_property
    def with_raw_response(self) -> AmlResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AmlResourceWithRawResponse(self)

    def screen(
        self, wallet_address: str, blockchain: str, *, timeout: float | None = None
    ) -> _types.AmlScreeningResult:
        """
        Выполняет AML-скрининг криптокошелька по адресу и сети.

        Пример запроса:
        POST /api/aml/screen
        { "walletAddress": "0x26a5919cd0392df875a53873b0323c42094bb216", "blockchain": "BNB" }

        Тарификация: списывается только успешный скрининг. Если сервис временно недоступен или
        входные данные некорректны, списания не происходит.

        Аргументы:
            wallet_address: Адрес криптокошелька для проверки (обязателен).
            blockchain: Сеть (блокчейн) адреса: "BTC", "ETH", "BNB", "TRX", "SOL" и т.д. (обязательно). Должна входить в список поддерживаемых сетей AmlBlockchains.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AmlScreeningResult",
            self._client.request(
                _screen_options(wallet_address=wallet_address, blockchain=blockchain, timeout=timeout)
            ),
        )

    def validate(
        self, wallet_address: str, blockchain: str, *, timeout: float | None = None
    ) -> _types.AmlValidationResult:
        """
        Проверяет входные данные AML-скрининга: поддержку сети и формат адреса.
        Проверяет формат, а не существование адреса в блокчейне.

        Пример запроса:
        GET /api/aml/validate?walletAddress=0x26a5919cd0392df875a53873b0323c42094bb216&blockchain=BNB

        Аргументы:
            wallet_address: Проверяемый адрес кошелька.
            blockchain: Код сети (например, "ETH", "BTC", "BNB").
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AmlValidationResult",
            self._client.request(
                _validate_options(wallet_address=wallet_address, blockchain=blockchain, timeout=timeout)
            ),
        )


class AsyncAmlResource(AsyncAPIResource):
    """
    API AML-скоринга.

    Примеры на шести языках: https://github.com/atlorium-api/aml-crypto-screening-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncAmlResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncAmlResourceWithRawResponse(self)

    async def screen(
        self, wallet_address: str, blockchain: str, *, timeout: float | None = None
    ) -> _types.AmlScreeningResult:
        """
        Выполняет AML-скрининг криптокошелька по адресу и сети.

        Пример запроса:
        POST /api/aml/screen
        { "walletAddress": "0x26a5919cd0392df875a53873b0323c42094bb216", "blockchain": "BNB" }

        Тарификация: списывается только успешный скрининг. Если сервис временно недоступен или
        входные данные некорректны, списания не происходит.

        Аргументы:
            wallet_address: Адрес криптокошелька для проверки (обязателен).
            blockchain: Сеть (блокчейн) адреса: "BTC", "ETH", "BNB", "TRX", "SOL" и т.д. (обязательно). Должна входить в список поддерживаемых сетей AmlBlockchains.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AmlScreeningResult",
            await self._client.request(
                _screen_options(wallet_address=wallet_address, blockchain=blockchain, timeout=timeout)
            ),
        )

    async def validate(
        self, wallet_address: str, blockchain: str, *, timeout: float | None = None
    ) -> _types.AmlValidationResult:
        """
        Проверяет входные данные AML-скрининга: поддержку сети и формат адреса.
        Проверяет формат, а не существование адреса в блокчейне.

        Пример запроса:
        GET /api/aml/validate?walletAddress=0x26a5919cd0392df875a53873b0323c42094bb216&blockchain=BNB

        Аргументы:
            wallet_address: Проверяемый адрес кошелька.
            blockchain: Код сети (например, "ETH", "BTC", "BNB").
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AmlValidationResult",
            await self._client.request(
                _validate_options(wallet_address=wallet_address, blockchain=blockchain, timeout=timeout)
            ),
        )


class AmlResourceWithRawResponse:
    """Методы :class:`AmlResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AmlResource) -> None:
        self.screen = to_raw_response_wrapper(resource.screen)
        self.validate = to_raw_response_wrapper(resource.validate)


class AsyncAmlResourceWithRawResponse:
    """Методы :class:`AsyncAmlResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncAmlResource) -> None:
        self.screen = to_async_raw_response_wrapper(resource.screen)
        self.validate = to_async_raw_response_wrapper(resource.validate)
