"""
Ресурс «API распознавания текста с изображения»: ``client.ocr``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._files import FileInput, encode_image
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import ocr as _types

__all__ = ["AsyncOcrResource", "OcrResource"]


def _recognize_options(*, image: FileInput, mode: str | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/ocr/image-to-text",
        json=strip_none({"image": encode_image(image), "mode": mode}),
        has_body=True,
        timeout=timeout,
        default_timeout=120,
    )


class OcrResource(SyncAPIResource):
    """
    API распознавания текста с изображения.

    Примеры на шести языках: https://github.com/atlorium-api/image-ocr-api-client
    """

    @cached_property
    def with_raw_response(self) -> OcrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return OcrResourceWithRawResponse(self)

    def recognize(
        self, image: FileInput, *, mode: str | None = None, timeout: float | None = None
    ) -> _types.ImageOcrResponse:
        """
        Распознаёт содержимое страницы на изображении. Изображение передаётся в Base64
        (можно как data-URL), предел — 10 МБ в декодированном виде.

        Пример запроса:
        POST /api/ocr/image-to-text
        { "image": "iVBORw0KGgoAAAANSUhEUgAA..." }

        Аргументы:
            image: Изображение в кодировке Base64 (можно как «голый» base64, так и data-URL вида "data:image/png;base64,...."). Обязательное поле. Предел — 10 МБ в декодированном виде: скан листа A4 в 300 dpi укладывается с запасом. PDF на вход не принимается — многостраничный файл нужно отрендерить в изображения и отправлять постранично.
            mode: Режим распознавания — одно из значений OcrModes. По умолчанию auto: сервис сам решает по размеру и содержимому изображения.  Указывать режим явно стоит в двух случаях: когда автоопределение промахивается на нетипичной картинке и когда важна предсказуемая стоимость — короткая строка всегда стоит одну единицу работы, а разбор страницы столько, сколько на ней областей.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.ImageOcrResponse", self._client.request(_recognize_options(image=image, mode=mode, timeout=timeout))
        )


class AsyncOcrResource(AsyncAPIResource):
    """
    API распознавания текста с изображения.

    Примеры на шести языках: https://github.com/atlorium-api/image-ocr-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncOcrResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncOcrResourceWithRawResponse(self)

    async def recognize(
        self, image: FileInput, *, mode: str | None = None, timeout: float | None = None
    ) -> _types.ImageOcrResponse:
        """
        Распознаёт содержимое страницы на изображении. Изображение передаётся в Base64
        (можно как data-URL), предел — 10 МБ в декодированном виде.

        Пример запроса:
        POST /api/ocr/image-to-text
        { "image": "iVBORw0KGgoAAAANSUhEUgAA..." }

        Аргументы:
            image: Изображение в кодировке Base64 (можно как «голый» base64, так и data-URL вида "data:image/png;base64,...."). Обязательное поле. Предел — 10 МБ в декодированном виде: скан листа A4 в 300 dpi укладывается с запасом. PDF на вход не принимается — многостраничный файл нужно отрендерить в изображения и отправлять постранично.
            mode: Режим распознавания — одно из значений OcrModes. По умолчанию auto: сервис сам решает по размеру и содержимому изображения.  Указывать режим явно стоит в двух случаях: когда автоопределение промахивается на нетипичной картинке и когда важна предсказуемая стоимость — короткая строка всегда стоит одну единицу работы, а разбор страницы столько, сколько на ней областей.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.ImageOcrResponse",
            await self._client.request(_recognize_options(image=image, mode=mode, timeout=timeout)),
        )


class OcrResourceWithRawResponse:
    """Методы :class:`OcrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: OcrResource) -> None:
        self.recognize = to_raw_response_wrapper(resource.recognize)


class AsyncOcrResourceWithRawResponse:
    """Методы :class:`AsyncOcrResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncOcrResource) -> None:
        self.recognize = to_async_raw_response_wrapper(resource.recognize)
