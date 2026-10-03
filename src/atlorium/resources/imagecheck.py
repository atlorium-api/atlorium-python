"""
Ресурс «API анализа изображения»: ``client.imagecheck``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._files import FileInput, encode_image
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import imagecheck as _types

__all__ = ["AsyncImageCheckResource", "ImageCheckResource"]


def _analyze_options(
    *, image: FileInput, include_text: bool | None, include_web_search: bool | None, timeout: float | None
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/imagecheck",
        json=strip_none(
            {"image": encode_image(image), "includeText": include_text, "includeWebSearch": include_web_search}
        ),
        has_body=True,
        timeout=timeout,
        default_timeout=60,
    )


class ImageCheckResource(SyncAPIResource):
    """
    API анализа изображения.

    Примеры на шести языках: https://github.com/atlorium-api/image-moderation-api-client
    """

    @cached_property
    def with_raw_response(self) -> ImageCheckResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return ImageCheckResourceWithRawResponse(self)

    def analyze(
        self,
        image: FileInput,
        *,
        include_text: bool | None = None,
        include_web_search: bool | None = None,
        timeout: float | None = None,
    ) -> _types.ImageModerationResult:
        """
        Анализирует изображение и возвращает решение модерации вместе с разбором содержимого.

        Пример запроса:

        POST /api/imagecheck
        {
          "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",
          "includeText": true,
          "includeWebSearch": false
        }

        ФОРМАТ ИЗОБРАЖЕНИЯ. Base64 — «голым» или в виде data-URL. Предел 7 МБ в декодированном
        виде. Принимаются JPEG, PNG, WEBP, BMP, GIF. PDF и видео на вход не подаются.

        КАК ЧИТАТЬ ОТВЕТ. Сначала decision — что делать. Затем flags — почему принято такое
        решение: у каждого срабатывания есть категория, слой-источник и конкретное
        доказательство (найденная метка, найденное в тексте выражение или категория
        классификации с её степенью). И только потом сырые слои, если решение нужно
        перепроверить или оспорить. Сырые слои отдаются намеренно: в модерации ошибка стоит
        дорого в обе стороны, и решение, которое нельзя проверить, доверия не заслуживает.

        ПУСТОЙ text — НЕ ОШИБКА. Он означает либо что читаемого текста на картинке нет, либо
        что слой не заказывался. Какой это случай, видно по billedUnits.

        ПАКЕТНОГО РЕЖИМА НЕТ намеренно: изображение — это мегабайты в теле запроса, и пакет
        превратился бы в стомегабайтный POST с таймаутами на промежуточных узлах. Поток
        модерируется параллельными одиночными запросами — они независимы, повторяются
        поштучно и не теряют весь пакет из-за одной битой картинки.

        ТАРИФИКАЦИЯ. От одной до трёх единиц, см. описание контроллера. Анализ, который
        не выполнен, не тарифицируется вовсе.

        Аргументы:
            image: Изображение в кодировке Base64 — «голым» base64 или data-URL вида data:image/jpeg;base64,.... Обязательное поле. Предел — 7 МБ в декодированном виде; фотография с телефона укладывается с запасом. Число нецелое не случайно: картинка уезжает в base64 внутри JSON-запроса, у которого чужой потолок 10 МБ, а кодирование добавляет около 37 %. Принимаются растровые форматы (JPEG, PNG, WEBP, BMP, GIF); PDF и видео на вход не подаются.
            include_text: Читать текст НА изображении и сверять его со словарём запрещённых выражений. Включено по умолчанию, и отключать это стоит с открытыми глазами.  ⚠️ Что перестаёт ловиться при false: скриншот с контактом продавца запрещённого, баннер казино, объявление о продаже документов, экстремистский лозунг поверх нейтральной картинки. На таких изображениях НЕ срабатывают ни классификация содержимого, ни метки предметов — там нет ни наготы, ни насилия, ни узнаваемого предмета. Текстовый слой для них единственный. В российских реалиях на него приходится значительная доля всего, что подлежит удалению.  Добавляет ОДНУ единицу работы. Отсутствие текста на изображении — нормальный исход, он тарифицируется: работа по чтению выполнена.
            include_web_search: Добавить поиск изображения в вебе: где ещё встречается эта картинка и какие страницы её содержат. Полезно против украденных фотографий в объявлениях и против контрафакта.  Самый дорогой из слоёв, поэтому выключен по умолчанию. Добавляет ОДНУ единицу работы. Если поиск не дал совпадений, единица за него не списывается — платить за пустой ответ клиент не должен.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.ImageModerationResult",
            self._client.request(
                _analyze_options(
                    image=image, include_text=include_text, include_web_search=include_web_search, timeout=timeout
                )
            ),
        )


class AsyncImageCheckResource(AsyncAPIResource):
    """
    API анализа изображения.

    Примеры на шести языках: https://github.com/atlorium-api/image-moderation-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncImageCheckResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncImageCheckResourceWithRawResponse(self)

    async def analyze(
        self,
        image: FileInput,
        *,
        include_text: bool | None = None,
        include_web_search: bool | None = None,
        timeout: float | None = None,
    ) -> _types.ImageModerationResult:
        """
        Анализирует изображение и возвращает решение модерации вместе с разбором содержимого.

        Пример запроса:

        POST /api/imagecheck
        {
          "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",
          "includeText": true,
          "includeWebSearch": false
        }

        ФОРМАТ ИЗОБРАЖЕНИЯ. Base64 — «голым» или в виде data-URL. Предел 7 МБ в декодированном
        виде. Принимаются JPEG, PNG, WEBP, BMP, GIF. PDF и видео на вход не подаются.

        КАК ЧИТАТЬ ОТВЕТ. Сначала decision — что делать. Затем flags — почему принято такое
        решение: у каждого срабатывания есть категория, слой-источник и конкретное
        доказательство (найденная метка, найденное в тексте выражение или категория
        классификации с её степенью). И только потом сырые слои, если решение нужно
        перепроверить или оспорить. Сырые слои отдаются намеренно: в модерации ошибка стоит
        дорого в обе стороны, и решение, которое нельзя проверить, доверия не заслуживает.

        ПУСТОЙ text — НЕ ОШИБКА. Он означает либо что читаемого текста на картинке нет, либо
        что слой не заказывался. Какой это случай, видно по billedUnits.

        ПАКЕТНОГО РЕЖИМА НЕТ намеренно: изображение — это мегабайты в теле запроса, и пакет
        превратился бы в стомегабайтный POST с таймаутами на промежуточных узлах. Поток
        модерируется параллельными одиночными запросами — они независимы, повторяются
        поштучно и не теряют весь пакет из-за одной битой картинки.

        ТАРИФИКАЦИЯ. От одной до трёх единиц, см. описание контроллера. Анализ, который
        не выполнен, не тарифицируется вовсе.

        Аргументы:
            image: Изображение в кодировке Base64 — «голым» base64 или data-URL вида data:image/jpeg;base64,.... Обязательное поле. Предел — 7 МБ в декодированном виде; фотография с телефона укладывается с запасом. Число нецелое не случайно: картинка уезжает в base64 внутри JSON-запроса, у которого чужой потолок 10 МБ, а кодирование добавляет около 37 %. Принимаются растровые форматы (JPEG, PNG, WEBP, BMP, GIF); PDF и видео на вход не подаются.
            include_text: Читать текст НА изображении и сверять его со словарём запрещённых выражений. Включено по умолчанию, и отключать это стоит с открытыми глазами.  ⚠️ Что перестаёт ловиться при false: скриншот с контактом продавца запрещённого, баннер казино, объявление о продаже документов, экстремистский лозунг поверх нейтральной картинки. На таких изображениях НЕ срабатывают ни классификация содержимого, ни метки предметов — там нет ни наготы, ни насилия, ни узнаваемого предмета. Текстовый слой для них единственный. В российских реалиях на него приходится значительная доля всего, что подлежит удалению.  Добавляет ОДНУ единицу работы. Отсутствие текста на изображении — нормальный исход, он тарифицируется: работа по чтению выполнена.
            include_web_search: Добавить поиск изображения в вебе: где ещё встречается эта картинка и какие страницы её содержат. Полезно против украденных фотографий в объявлениях и против контрафакта.  Самый дорогой из слоёв, поэтому выключен по умолчанию. Добавляет ОДНУ единицу работы. Если поиск не дал совпадений, единица за него не списывается — платить за пустой ответ клиент не должен.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.ImageModerationResult",
            await self._client.request(
                _analyze_options(
                    image=image, include_text=include_text, include_web_search=include_web_search, timeout=timeout
                )
            ),
        )


class ImageCheckResourceWithRawResponse:
    """Методы :class:`ImageCheckResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: ImageCheckResource) -> None:
        self.analyze = to_raw_response_wrapper(resource.analyze)


class AsyncImageCheckResourceWithRawResponse:
    """Методы :class:`AsyncImageCheckResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncImageCheckResource) -> None:
        self.analyze = to_async_raw_response_wrapper(resource.analyze)
