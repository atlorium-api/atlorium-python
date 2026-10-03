"""
Ресурс «API разбора Cron-выражений»: ``client.cron``.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from functools import cached_property
from typing import cast

from .._base_client import RequestOptions
from .._resource import AsyncAPIResource, SyncAPIResource, strip_none
from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper
from ..types import cron as _types

__all__ = ["AsyncCronResource", "CronResource"]


def _evaluate_options(
    *,
    expression: str,
    time_zone_id: str | None,
    from_utc: datetime | str | None,
    take: int | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/cron/evaluate",
        json=strip_none({"expression": expression, "timeZoneId": time_zone_id, "fromUtc": from_utc, "take": take}),
        has_body=True,
        timeout=timeout,
    )


def _build_options(
    *,
    template: int | None,
    interval: int | None,
    time_of_day: str | None,
    day_of_month: int | None,
    week_days: Sequence[int] | None,
    include_seconds: bool | None,
    timeout: float | None,
) -> RequestOptions:
    return RequestOptions(
        method="POST",
        path="/api/cron/build",
        json=strip_none(
            {
                "template": template,
                "interval": interval,
                "timeOfDay": time_of_day,
                "dayOfMonth": day_of_month,
                "weekDays": None if week_days is None else list(week_days),
                "includeSeconds": include_seconds,
            }
        ),
        has_body=True,
        timeout=timeout,
    )


class CronResource(SyncAPIResource):
    """
    API разбора Cron-выражений.

    Примеры на шести языках: https://github.com/atlorium-api/cron-expression-parser-api-client
    """

    @cached_property
    def with_raw_response(self) -> CronResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return CronResourceWithRawResponse(self)

    def evaluate(
        self,
        expression: str,
        *,
        time_zone_id: str | None = None,
        from_utc: datetime | str | None = None,
        take: int | None = None,
        timeout: float | None = None,
    ) -> _types.CronEvaluationResult:
        """
        Парсит и валидирует cron-выражение, возвращает ближайшие даты запуска.
        Позволяет проверить корректность выражения и увидеть, когда оно сработает.

        Пример запроса:
        POST /api/cron/evaluate
        Body: {
          "expression": "0 9 * * 1-5",
          "timeZoneId": "Europe/Moscow",
          "take": 5
        }

        Пример ответа:
        {
          "isValid": true,
          "description": "В 09:00, по будням с понедельника по пятницу",
          "nextOccurrences": ["2024-01-15T09:00:00+03:00", ...]
        }

        Аргументы:
            expression: Cron-выражение (5 или 6 полей, допускается ? из Quartz).
            time_zone_id: Часовой пояс для расчёта (Id из TimeZoneInfo).
            from_utc: Стартовая точка расчёта (UTC). Если не задана — сейчас.
            take: Количество ближайших запусков (1-100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CronEvaluationResult",
            self._client.request(
                _evaluate_options(
                    expression=expression, time_zone_id=time_zone_id, from_utc=from_utc, take=take, timeout=timeout
                )
            ),
        )

    def build(
        self,
        *,
        template: int | None = None,
        interval: int | None = None,
        time_of_day: str | None = None,
        day_of_month: int | None = None,
        week_days: Sequence[int] | None = None,
        include_seconds: bool | None = None,
        timeout: float | None = None,
    ) -> _types.CronBuildResult:
        """
        Генерирует cron-строку по заданному шаблону и параметрам.
        Упрощает создание cron-выражений для типовых сценариев.

        Аргументы:
            template: Заготовка расписания. От неё зависит, какие из остальных полей вообще учитываются: интервал нужен только шаблонам с шагом, дни недели — недельному, число месяца — месячному.
            interval: Шаг для шаблонов «каждые N минут» и «каждые N часов»; остальными шаблонами игнорируется. Пример: шаблон «каждые N минут» с интервалом 15 даёт в поле минут */15.
            time_of_day: Время суток для суточного, недельного и месячного расписаний. Например, 09:30 — запуск в половине десятого утра.
            day_of_month: Число месяца (1–31) для месячного расписания. Учитывайте короткие месяцы: 31-е число пропустит февраль, апрель, июнь, сентябрь и ноябрь.
            week_days: Дни недели для недельного расписания. Можно выбрать несколько — запуск произойдёт в каждый из них.
            include_seconds: Добавлять ли в выражение поле секунд. true даёт шесть полей (диалект Quartz), false — классические пять полей Unix cron. Выбирать нужно по тому планировщику, куда выражение потом вставят: лишнее поле секунд он разберёт неверно.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CronBuildResult",
            self._client.request(
                _build_options(
                    template=template,
                    interval=interval,
                    time_of_day=time_of_day,
                    day_of_month=day_of_month,
                    week_days=week_days,
                    include_seconds=include_seconds,
                    timeout=timeout,
                )
            ),
        )


class AsyncCronResource(AsyncAPIResource):
    """
    API разбора Cron-выражений.

    Примеры на шести языках: https://github.com/atlorium-api/cron-expression-parser-api-client
    """

    @cached_property
    def with_raw_response(self) -> AsyncCronResourceWithRawResponse:
        """Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."""
        return AsyncCronResourceWithRawResponse(self)

    async def evaluate(
        self,
        expression: str,
        *,
        time_zone_id: str | None = None,
        from_utc: datetime | str | None = None,
        take: int | None = None,
        timeout: float | None = None,
    ) -> _types.CronEvaluationResult:
        """
        Парсит и валидирует cron-выражение, возвращает ближайшие даты запуска.
        Позволяет проверить корректность выражения и увидеть, когда оно сработает.

        Пример запроса:
        POST /api/cron/evaluate
        Body: {
          "expression": "0 9 * * 1-5",
          "timeZoneId": "Europe/Moscow",
          "take": 5
        }

        Пример ответа:
        {
          "isValid": true,
          "description": "В 09:00, по будням с понедельника по пятницу",
          "nextOccurrences": ["2024-01-15T09:00:00+03:00", ...]
        }

        Аргументы:
            expression: Cron-выражение (5 или 6 полей, допускается ? из Quartz).
            time_zone_id: Часовой пояс для расчёта (Id из TimeZoneInfo).
            from_utc: Стартовая точка расчёта (UTC). Если не задана — сейчас.
            take: Количество ближайших запусков (1-100).
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CronEvaluationResult",
            await self._client.request(
                _evaluate_options(
                    expression=expression, time_zone_id=time_zone_id, from_utc=from_utc, take=take, timeout=timeout
                )
            ),
        )

    async def build(
        self,
        *,
        template: int | None = None,
        interval: int | None = None,
        time_of_day: str | None = None,
        day_of_month: int | None = None,
        week_days: Sequence[int] | None = None,
        include_seconds: bool | None = None,
        timeout: float | None = None,
    ) -> _types.CronBuildResult:
        """
        Генерирует cron-строку по заданному шаблону и параметрам.
        Упрощает создание cron-выражений для типовых сценариев.

        Аргументы:
            template: Заготовка расписания. От неё зависит, какие из остальных полей вообще учитываются: интервал нужен только шаблонам с шагом, дни недели — недельному, число месяца — месячному.
            interval: Шаг для шаблонов «каждые N минут» и «каждые N часов»; остальными шаблонами игнорируется. Пример: шаблон «каждые N минут» с интервалом 15 даёт в поле минут */15.
            time_of_day: Время суток для суточного, недельного и месячного расписаний. Например, 09:30 — запуск в половине десятого утра.
            day_of_month: Число месяца (1–31) для месячного расписания. Учитывайте короткие месяцы: 31-е число пропустит февраль, апрель, июнь, сентябрь и ноябрь.
            week_days: Дни недели для недельного расписания. Можно выбрать несколько — запуск произойдёт в каждый из них.
            include_seconds: Добавлять ли в выражение поле секунд. true даёт шесть полей (диалект Quartz), false — классические пять полей Unix cron. Выбирать нужно по тому планировщику, куда выражение потом вставят: лишнее поле секунд он разберёт неверно.
            timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).
        """
        return cast(
            "_types.CronBuildResult",
            await self._client.request(
                _build_options(
                    template=template,
                    interval=interval,
                    time_of_day=time_of_day,
                    day_of_month=day_of_month,
                    week_days=week_days,
                    include_seconds=include_seconds,
                    timeout=timeout,
                )
            ),
        )


class CronResourceWithRawResponse:
    """Методы :class:`CronResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: CronResource) -> None:
        self.evaluate = to_raw_response_wrapper(resource.evaluate)
        self.build = to_raw_response_wrapper(resource.build)


class AsyncCronResourceWithRawResponse:
    """Методы :class:`AsyncCronResource`, возвращающие :class:`~atlorium.ApiResponse`."""

    def __init__(self, resource: AsyncCronResource) -> None:
        self.evaluate = to_async_raw_response_wrapper(resource.evaluate)
        self.build = to_async_raw_response_wrapper(resource.build)
