"""
Ресурс «API ИИ-чата»: ``client.aichat``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import cast

from .._base_client import RequestOptions, path_segment
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import aichat as _types

__all__ = ["AiChatResource", "AsyncAiChatResource"]


def _send_options(*, message: str, session_id: str | None, model: str | None, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/aichat/send",
        json=strip_none({"message": message, "sessionId": session_id, "model": model}),
        has_body=True,
        timeout=timeout,
        default_timeout=660,
    )


def _get_session_options(*, session_id: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path=f"/api/aichat/session/{path_segment(session_id)}", timeout=timeout)


def _delete_session_options(*, session_id: str, timeout: float | None) -> RequestOptions:
    return RequestOptions(
        method="DELETE", path=f"/api/aichat/session/{path_segment(session_id)}", timeout=timeout, response_type="auto"
    )


def _list_models_options(*, timeout: float | None) -> RequestOptions:
    return RequestOptions(method="GET", path="/api/aichat/models", timeout=timeout)


class AiChatResource(SyncAPIResource):
    """
    API ИИ-чата.

    Примеры на шести языках: https://github.com/atlorium-api/ai-chat-api-client
    """

    @cached_property
    def with_raw_response(self) -> AiChatResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AiChatResourceWithRawResponse(self)

    def send(
        self, message: str, *, session_id: str | None = None, model: str | None = None, timeout: float | None = None
    ) -> _types.AiChatResponse:
        """
        Отправляет сообщение ИИ и получает ответ.
        Автоматически создаёт новую сессию или продолжает существующую.

        Пример запроса:
        POST /api/aichat/send
        Content-Type: application/json

        {
          "message": "Что такое DNS?",
          "sessionId": null
        }

        Для продолжения диалога передайте sessionId из предыдущего ответа:
        {
          "message": "А как работает DNSSEC?",
          "sessionId": "abc123def456"
        }

        Ограничения:
        - Длина сообщения ограничена в токенах и зависит от модели (см. maxInputTokens в GET /api/aichat/models)
        - Максимум 50 сообщений пользователя в одной сессии
        - Сессия удаляется через 1 час неактивности
        - Поле model принимает только модели из GET /api/aichat/models; произвольное имя — 400

        ТАРИФИКАЦИЯ складывается из ДВУХ составляющих:
        1) плата за запрос — фиксированная, одинаковая для всех моделей;
        2) стоимость токенов выбранной модели — зависит от модели и от длины диалога.
           У бесплатных моделей она равна нулю, и тогда вы платите только за запрос.
           Цены токенов каждой модели — в GET /api/aichat/models (inputPricePer1kTokens,
           outputPricePer1kTokens) и на странице тарифов.

        В ответе возвращаются фактически израсходованные токены (promptTokens/completionTokens) —
        именно по ним и считается вторая составляющая.

        ВАЖНО ПРО БАЛАНС: перед вызовом модели временно удерживается максимально возможная
        стоимость запроса (весь ввод + самый длинный ответ), а списывается только фактически
        израсходованное — остаток удержания сразу возвращается. Поэтому для запроса к дорогой
        модели на балансе должен быть этот максимум, даже если по факту спишется меньше.
        Если баланса не хватает на удержание — 402 Payment Required.

        ВРЕМЯ ОТВЕТА: ответ приходит целиком, а не частями, и перед ответом модель рассуждает.
        Короткий ответ приходит за секунды, развёрнутый ответ флагманской модели — за несколько
        минут. Ставьте таймаут HTTP-клиента не меньше 10 минут: если клиент оборвёт соединение
        раньше, модель всё равно допишет ответ, и запрос будет оплачен как выполненный.
        Не тарифицируются только сбои: модель не ответила за 10 минут или вернула ответ без
        текста (израсходовала лимит ответа на рассуждения) — в обоих случаях код 500.

        Аргументы:
            message: Текст сообщения пользователя (обязательное поле; длина ограничена в зависимости от выбранной модели).
            session_id: Идентификатор существующей сессии для продолжения диалога. Если null — сервис автоматически создаст новую сессию.
            model: Идентификатор или алиас ИИ модели для обработки запроса. Если null — используется модель по умолчанию из конфигурации сервера. Список доступных моделей можно получить через GET /api/aichat/models.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AiChatResponse",
            self._client.request(_send_options(message=message, session_id=session_id, model=model, timeout=timeout)),
        )

    def get_session(self, session_id: str, *, timeout: float | None = None) -> _types.AiChatSession:
        """
        Получает информацию о сессии чата по её идентификатору.
        Возвращает количество сообщений, время создания и последней активности.

        Пример запроса:
        GET /api/aichat/session/abc123def456789012345678abcdef00

        Сессии сохраняются и автоматически удаляются через 1 час неактивности.

        Аргументы:
            session_id: Уникальный идентификатор сессии чата.  Формат: строка из 32 шестнадцатеричных символов (GUID без дефисов).  Пример: abc123def456789012345678abcdef00  Идентификатор возвращается в ответе метода SendMessage при создании новой сессии.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AiChatSession", self._client.request(_get_session_options(session_id=session_id, timeout=timeout))
        )

    def delete_session(self, session_id: str, *, timeout: float | None = None) -> str:
        """
        Удаляет сессию чата и всю историю сообщений.
        После удаления сессию невозможно восстановить.

        Пример запроса:
        DELETE /api/aichat/session/abc123def456789012345678abcdef00

        После удаления все сообщения сессии безвозвратно удаляются.
        Повторная отправка сообщения с тем же sessionId создаст новую пустую сессию.

        Аргументы:
            session_id: Уникальный идентификатор сессии чата для удаления.  Формат: строка из 32 шестнадцатеричных символов (GUID без дефисов).  Пример: abc123def456789012345678abcdef00
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("str", self._client.request(_delete_session_options(session_id=session_id, timeout=timeout)))

    def list_models(self, *, timeout: float | None = None) -> list[_types.AiModelInfo]:
        """
        Возвращает список доступных ИИ моделей.
        Каждая модель имеет уникальный идентификатор, название, описание и лимит токенов.

        Пример запроса:
        GET /api/aichat/models

        Список моделей может меняться. Этот метод бесплатный и не тарифицируется —
        тарифицируется только POST /api/aichat/send. Чтобы обратиться к конкретной модели,
        передайте её id в поле model запроса на отправку сообщения.

        Стоимость запроса к /api/aichat/send складывается из двух частей: фиксированной платы
        за запрос (одинаковой для всех моделей) и стоимости токенов выбранной модели —
        она у моделей РАЗНАЯ (inputPricePer1kTokens/outputPricePer1kTokens ниже, для бесплатных
        моделей — ноль). Подробности — в описании метода POST /api/aichat/send.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("list[_types.AiModelInfo]", self._client.request(_list_models_options(timeout=timeout)))


class AsyncAiChatResource(AsyncAPIResource):
    """
    API ИИ-чата.

    Примеры на шести языках: https://github.com/atlorium-api/ai-chat-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncAiChatResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncAiChatResourceWithRawResponse(self)

    async def send(
        self, message: str, *, session_id: str | None = None, model: str | None = None, timeout: float | None = None
    ) -> _types.AiChatResponse:
        """
        Отправляет сообщение ИИ и получает ответ.
        Автоматически создаёт новую сессию или продолжает существующую.

        Пример запроса:
        POST /api/aichat/send
        Content-Type: application/json

        {
          "message": "Что такое DNS?",
          "sessionId": null
        }

        Для продолжения диалога передайте sessionId из предыдущего ответа:
        {
          "message": "А как работает DNSSEC?",
          "sessionId": "abc123def456"
        }

        Ограничения:
        - Длина сообщения ограничена в токенах и зависит от модели (см. maxInputTokens в GET /api/aichat/models)
        - Максимум 50 сообщений пользователя в одной сессии
        - Сессия удаляется через 1 час неактивности
        - Поле model принимает только модели из GET /api/aichat/models; произвольное имя — 400

        ТАРИФИКАЦИЯ складывается из ДВУХ составляющих:
        1) плата за запрос — фиксированная, одинаковая для всех моделей;
        2) стоимость токенов выбранной модели — зависит от модели и от длины диалога.
           У бесплатных моделей она равна нулю, и тогда вы платите только за запрос.
           Цены токенов каждой модели — в GET /api/aichat/models (inputPricePer1kTokens,
           outputPricePer1kTokens) и на странице тарифов.

        В ответе возвращаются фактически израсходованные токены (promptTokens/completionTokens) —
        именно по ним и считается вторая составляющая.

        ВАЖНО ПРО БАЛАНС: перед вызовом модели временно удерживается максимально возможная
        стоимость запроса (весь ввод + самый длинный ответ), а списывается только фактически
        израсходованное — остаток удержания сразу возвращается. Поэтому для запроса к дорогой
        модели на балансе должен быть этот максимум, даже если по факту спишется меньше.
        Если баланса не хватает на удержание — 402 Payment Required.

        ВРЕМЯ ОТВЕТА: ответ приходит целиком, а не частями, и перед ответом модель рассуждает.
        Короткий ответ приходит за секунды, развёрнутый ответ флагманской модели — за несколько
        минут. Ставьте таймаут HTTP-клиента не меньше 10 минут: если клиент оборвёт соединение
        раньше, модель всё равно допишет ответ, и запрос будет оплачен как выполненный.
        Не тарифицируются только сбои: модель не ответила за 10 минут или вернула ответ без
        текста (израсходовала лимит ответа на рассуждения) — в обоих случаях код 500.

        Аргументы:
            message: Текст сообщения пользователя (обязательное поле; длина ограничена в зависимости от выбранной модели).
            session_id: Идентификатор существующей сессии для продолжения диалога. Если null — сервис автоматически создаст новую сессию.
            model: Идентификатор или алиас ИИ модели для обработки запроса. Если null — используется модель по умолчанию из конфигурации сервера. Список доступных моделей можно получить через GET /api/aichat/models.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AiChatResponse",
            await self._client.request(
                _send_options(message=message, session_id=session_id, model=model, timeout=timeout)
            ),
        )

    async def get_session(self, session_id: str, *, timeout: float | None = None) -> _types.AiChatSession:
        """
        Получает информацию о сессии чата по её идентификатору.
        Возвращает количество сообщений, время создания и последней активности.

        Пример запроса:
        GET /api/aichat/session/abc123def456789012345678abcdef00

        Сессии сохраняются и автоматически удаляются через 1 час неактивности.

        Аргументы:
            session_id: Уникальный идентификатор сессии чата.  Формат: строка из 32 шестнадцатеричных символов (GUID без дефисов).  Пример: abc123def456789012345678abcdef00  Идентификатор возвращается в ответе метода SendMessage при создании новой сессии.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.AiChatSession",
            await self._client.request(_get_session_options(session_id=session_id, timeout=timeout)),
        )

    async def delete_session(self, session_id: str, *, timeout: float | None = None) -> str:
        """
        Удаляет сессию чата и всю историю сообщений.
        После удаления сессию невозможно восстановить.

        Пример запроса:
        DELETE /api/aichat/session/abc123def456789012345678abcdef00

        После удаления все сообщения сессии безвозвратно удаляются.
        Повторная отправка сообщения с тем же sessionId создаст новую пустую сессию.

        Аргументы:
            session_id: Уникальный идентификатор сессии чата для удаления.  Формат: строка из 32 шестнадцатеричных символов (GUID без дефисов).  Пример: abc123def456789012345678abcdef00
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("str", await self._client.request(_delete_session_options(session_id=session_id, timeout=timeout)))

    async def list_models(self, *, timeout: float | None = None) -> list[_types.AiModelInfo]:
        """
        Возвращает список доступных ИИ моделей.
        Каждая модель имеет уникальный идентификатор, название, описание и лимит токенов.

        Пример запроса:
        GET /api/aichat/models

        Список моделей может меняться. Этот метод бесплатный и не тарифицируется —
        тарифицируется только POST /api/aichat/send. Чтобы обратиться к конкретной модели,
        передайте её id в поле model запроса на отправку сообщения.

        Стоимость запроса к /api/aichat/send складывается из двух частей: фиксированной платы
        за запрос (одинаковой для всех моделей) и стоимости токенов выбранной модели —
        она у моделей РАЗНАЯ (inputPricePer1kTokens/outputPricePer1kTokens ниже, для бесплатных
        моделей — ноль). Подробности — в описании метода POST /api/aichat/send.

        Аргументы:
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast("list[_types.AiModelInfo]", await self._client.request(_list_models_options(timeout=timeout)))


class AiChatResourceWithRawResponse:
    """Методы :class:`AiChatResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AiChatResource) -> None:
        self.send = to_raw_response_wrapper(resource.send)
        self.get_session = to_raw_response_wrapper(resource.get_session)
        self.delete_session = to_raw_response_wrapper(resource.delete_session)
        self.list_models = to_raw_response_wrapper(resource.list_models)


class AsyncAiChatResourceWithRawResponse:
    """Методы :class:`AsyncAiChatResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncAiChatResource) -> None:
        self.send = to_async_raw_response_wrapper(resource.send)
        self.get_session = to_async_raw_response_wrapper(resource.get_session)
        self.delete_session = to_async_raw_response_wrapper(resource.delete_session)
        self.list_models = to_async_raw_response_wrapper(resource.list_models)
