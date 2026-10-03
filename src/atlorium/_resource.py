"""Базовые классы ресурсов: ресурс держит ссылку на клиент и отправляет через него запросы."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._base_client import AsyncAPIClient, SyncAPIClient

__all__ = ["AsyncAPIResource", "SyncAPIResource", "strip_none"]


class SyncAPIResource:
    """Ресурс синхронного клиента (один сервис Atlorium)."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client


class AsyncAPIResource:
    """Ресурс асинхронного клиента (один сервис Atlorium)."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client


def strip_none(values: dict[str, Any]) -> dict[str, Any]:
    """Убирает из тела запроса непереданные (``None``) поля — тогда действует серверный дефолт."""
    return {key: value for key, value in values.items() if value is not None}
