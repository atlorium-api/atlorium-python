"""
Типы запросов и ответов сервиса «API калькулятора подсетей».

Модели ответов — ``TypedDict`` (обычные ``dict``): новые поля сервера не ломают разбор.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками. Источник: spec/cidr_ru.json.
"""

from __future__ import annotations

from typing import TypedDict


class ApiError(TypedDict, total=False):
    """Единое тело ответа для любого отказа: и для ошибки валидации, и для отсутствующего ключа, и для исчерпанного лимита. Ветвиться в коде следует по полю `error` — это стабильный машинный код. Поля `title` и `message` предназначены человеку, их формулировки могут меняться."""

    error: str
    """
    Машинный код причины отказа. Возможные значения:

    * `server_error` (500) — Сервис временно недоступен
    * `unauthorized` (401) — Требуется вход
    * `api_key_required` (401) — Нужен API-ключ
    * `account_not_activated` (402) — Аккаунт не активирован
    * `rate_limited_client` (429) — Слишком много запросов
    * `rate_limited_global` (429) — Высокая нагрузка на сервис
    * `provider_keys_exhausted` (429) — Сервис временно недоступен
    * `insufficient_credits` (402) — Недостаточно кредитов
    * `guest_quota_exhausted` (402) — Бесплатный лимит на сегодня исчерпан
    * `service_disabled` (503) — Проводятся плановые работы
    * `maintenance` (503) — Проводятся плановые работы
    * `guest_not_allowed` (402) — Нужна регистрация
    * `service_not_in_account_terms` (403) — Сервис не подключён
    * `bad_request` (400) — Некорректный запрос
    * `forbidden` (403) — Доступ запрещён
    * `not_found` (404) — Ничего не найдено
    * `method_not_allowed` (405) — Метод HTTP не поддерживается
    * `unsupported_media_type` (415) — Формат запроса не поддерживается
    * `not_implemented` (501) — Режим пока не реализован
    """

    title: str
    """Короткий заголовок для интерфейса."""

    message: str
    """Подробное объяснение: что произошло и что с этим делать. Показывается пользователю целиком."""

    balance: float | None
    """Текущий баланс в кредитах. Заполняется при 402, чтобы не делать отдельный запрос за балансом; в остальных случаях null."""

    retryAfterSeconds: float | None
    """Через сколько секунд имеет смысл повторить запрос. Дублирует HTTP-заголовок Retry-After. null — если повтор не поможет (например, кончились кредиты)."""

    retryAfterText: str | None
    """Та же задержка готовой фразой — «через 2 мин 30 с». Чтобы клиентам не приходилось самим склонять минуты и секунды."""


class CidrCalculationResult(TypedDict, total=False):
    """Результат расчёта CIDR — содержит все вычисленные параметры сети."""

    ipAddress: str
    """Исходный IP-адрес, введённый пользователем."""

    mask: int
    """Маска подсети в CIDR-нотации (например, 24 для /24)."""

    ipVersion: int
    """Версия IP-протокола: 4 для IPv4, 6 для IPv6."""

    networkAddress: str
    """Адрес сети (Network Address) — первый адрес в диапазоне."""

    broadcastAddress: str
    """
    Широковещательный адрес (Broadcast Address) — последний адрес в диапазоне.
    Для IPv6 технически не существует, но возвращаем последний адрес диапазона.
    """

    netmask: str
    """Маска подсети в полном формате (например, 255.255.255.0)."""

    wildcardMask: str
    """Wildcard-маска — инверсия маски подсети (используется в ACL Cisco)."""

    firstUsableIp: str
    """Первый используемый IP-адрес (Network + 1 для IPv4)."""

    lastUsableIp: str
    """Последний используемый IP-адрес (Broadcast - 1 для IPv4)."""

    totalHosts: str
    """
    Общее количество хостов в сети.
    Для больших IPv6 сетей возвращается строка, так как BigInteger.
    """

    usableHosts: str
    """Количество используемых хостов (без Network и Broadcast для IPv4)."""

    cidrNotation: str
    """CIDR-нотация сети (например, 192.168.1.0/24)."""

    binaryRepresentation: str
    """Двоичное представление IP-адреса."""

    hexRepresentation: str
    """Шестнадцатеричное представление IP-адреса."""

    binaryMask: str
    """Двоичное представление маски подсети."""

    success: bool
    """Флаг успешности расчёта."""

    error: str | None
    """Сообщение об ошибке, если расчёт не удался."""


class IpRangeCheckResult(TypedDict, total=False):
    """Результат проверки принадлежности IP-адреса к CIDR-диапазону."""

    cidr: str
    """Проверяемый CIDR-диапазон."""

    ipAddress: str
    """Проверяемый IP-адрес."""

    isInRange: bool
    """Результат проверки: true — IP находится в диапазоне."""

    details: str
    """Детальное описание результата проверки."""

    success: bool
    """Флаг успешности проверки (валидность входных данных)."""

    error: str | None
    """Сообщение об ошибке, если проверка не удалась."""


class SubnetInfo(TypedDict, total=False):
    """Информация об отдельной подсети."""

    index: int
    """Порядковый номер подсети (начиная с 1)."""

    networkAddress: str
    """Адрес сети."""

    broadcastAddress: str
    """Широковещательный адрес."""

    firstUsableIp: str
    """Первый используемый IP-адрес."""

    lastUsableIp: str
    """Последний используемый IP-адрес."""

    hostCount: str
    """Количество хостов в подсети."""

    cidrNotation: str
    """CIDR-нотация подсети."""


class SubnetBreakdownResult(TypedDict, total=False):
    """Результат разбиения сети на подсети."""

    originalCidr: str
    """Исходный CIDR, который разбивается на подсети."""

    newMask: int
    """Новая маска для подсетей."""

    totalSubnets: str
    """Общее количество возможных подсетей."""

    displayedCount: int
    """Количество отображаемых подсетей (до 128)."""

    isTruncated: bool
    """Флаг, указывающий что результат был ограничен."""

    subnets: list[SubnetInfo]
    """Список подсетей."""

    success: bool
    """Флаг успешности расчёта."""

    error: str | None
    """Сообщение об ошибке, если расчёт не удался."""


class SupernetRequest(TypedDict, total=False):
    """Запрос на агрегацию CIDR/IP."""

    inputs: list[str]
    """
    Список входных IP-адресов и/или CIDR для агрегации.
    Поддерживаемые разделители: новая строка, запятая, точка с запятой, пробел.
    """


class SupernetResult(TypedDict, total=False):
    """Результат агрегации (supernetting) — наименьший общий CIDR."""

    inputs: list[str]
    """Список входных IP-адресов и CIDR."""

    parsedCount: int
    """Количество успешно разобранных входных значений."""

    supernetCidr: str
    """Вычисленный агрегированный CIDR (Supernet)."""

    networkAddress: str
    """Адрес сети supernet."""

    broadcastAddress: str
    """Широковещательный адрес supernet."""

    totalHosts: str
    """Общее количество хостов в supernet."""

    success: bool
    """Флаг успешности расчёта."""

    error: str | None
    """Сообщение об ошибке, если расчёт не удался."""

    warnings: list[str]
    """Список предупреждений (например, если некоторые входные значения не распознаны)."""


__all__ = [
    "ApiError",
    "CidrCalculationResult",
    "IpRangeCheckResult",
    "SubnetBreakdownResult",
    "SubnetInfo",
    "SupernetRequest",
    "SupernetResult",
]
