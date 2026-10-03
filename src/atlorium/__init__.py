"""
Официальный Python SDK для Atlorium — 23 B2B API для российского рынка.

    from atlorium import Atlorium

    client = Atlorium()  # без ключа работает на демо-ключе: ответы — детерминированные моки
    card = client.egrul.get("7707083893")

Документация: https://atlorium.com, исходники: https://github.com/atlorium-api/atlorium-python
"""

from ._base_client import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    SANDBOX_API_KEY,
    AtloriumSandboxWarning,
)
from ._client import AsyncAtlorium, Atlorium
from ._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AtloriumError,
    AuthenticationError,
    InsufficientCreditsError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
    ValidationError,
)
from ._files import FileInput
from ._response import ApiResponse, RateLimitInfo
from ._version import __version__

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "SANDBOX_API_KEY",
    "APIConnectionError",
    "APITimeoutError",
    "ApiResponse",
    "AsyncAtlorium",
    "Atlorium",
    "AtloriumError",
    "AtloriumSandboxWarning",
    "AuthenticationError",
    "FileInput",
    "InsufficientCreditsError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "RateLimitInfo",
    "ServerError",
    "ServiceUnavailableError",
    "ValidationError",
    "__version__",
]
