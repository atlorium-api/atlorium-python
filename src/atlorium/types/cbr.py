"""
Типы запросов и ответов сервиса «API справочника БИК».

Модели ответов — ``TypedDict`` (обычные ``dict``): новые поля сервера не ломают разбор.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками. Источник: spec/cbr_ru.json.
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


class CbrAccountRestriction(TypedDict, total=False):
    """Ограничение на уровне счёта (элемент <AccRstrList> внутри <Accounts>)."""

    code: str
    """Код ограничения по счёту (AccRstrList@AccRstr) в исходном виде справочника."""

    date: str | None
    """Дата введения ограничения по счёту (AccRstrList@AccRstrDate). null, если не указана."""

    successorBic: str | None
    """
    БИК подразделения/счёта-правопреемника (AccRstrList@SuccessorBIC), если счёт переведён.
    null, если правопреемника нет.
    """


class CbrAccount(TypedDict, total=False):
    """
    Счёт участника справочника БИК (элемент <Accounts> внутри BICDirectoryEntry).
    Содержит реквизиты, нужные для формирования платёжных поручений.
    """

    account: str
    """Номер счёта (Accounts@Account, 20 цифр)."""

    accountType: str | None
    """
    Тип счёта по классификации ЦБ (Accounts@RegulationAccountType): "CRSA" — корреспондентский
    счёт, "CRSS" — субсчёт и т.п. Позволяет отличить основной корсчёт от прочих счетов.
    """

    controlKey: str | None
    """Контрольный ключ счёта (Accounts@CK). Используется при проверке реквизитов платежа."""

    cbrBic: str | None
    """БИК подразделения Банка России, в котором открыт счёт (Accounts@AccountCBRBIC)."""

    status: str | None
    """
    Статус счёта (Accounts@AccountStatus): "ACAC" — действующий. Прочие значения означают
    закрытый/недействующий счёт. Возвращается в исходном виде справочника.
    """

    dateIn: str | None
    """Дата открытия счёта (Accounts@DateIn). null, если не указана."""

    restrictions: list[CbrAccountRestriction]
    """
    Ограничения на уровне счёта (элементы <AccRstrList> внутри <Accounts>). Например,
    при переводе счёта на обслуживание в другое подразделение указывается счёт-правопреемник.
    Пустой список — ограничений по счёту нет.
    """


class CbrRestriction(TypedDict, total=False):
    """Ограничение, наложенное на участника справочника БИК (элемент <RstrList>)."""

    code: str
    """
    Код ограничения (RstrList@Rstr). Примеры: "URRS" — отзыв лицензии, "LWRS" — ликвидация,
    "MRTS" — мораторий. Код возвращается в исходном виде и сопоставляется со справочником
    кодов ограничений Банка России.
    """

    date: str | None
    """Дата введения ограничения (RstrList@RstrDate). null, если не указана."""


class CbrBankInfo(TypedDict, total=False):
    """
    Карточка одного участника справочника БИК: банка, филиала, РКЦ, УФК и т.п.
    Содержит реквизиты записи справочника Банка России одним плоским набором полей —
    наименование и адрес участника, счета, коды SWIFT и действующие ограничения.
    """

    bik: str
    """БИК — банковский идентификационный код (9 цифр). Атрибут BIC у BICDirectoryEntry."""

    name: str
    """Наименование участника (ParticipantInfo@NameP)."""

    englishName: str | None
    """Наименование участника на английском (ParticipantInfo@EnglName). Есть не у всех."""

    corrAccount: str | None
    """
    Корреспондентский счёт участника (счёт из <Accounts> с типом RegulationAccountType="CRSA").
    Это основной корреспондентский счёт участника; полный список счетов — в accounts.
    Для участников без корсчёта (УФК, некоторые подразделения) — null.
    """

    countryCode: str | None
    """Код страны участника по ISO-3166 alpha-2 (ParticipantInfo@CntrCd, обычно "RU")."""

    parentBic: str | None
    """
    БИК головной организации (ParticipantInfo@PrntBIC). Заполнен у филиалов и подразделений —
    указывает на головной банк. У головных банков обычно отсутствует. Удобно для связки «филиал → банк».
    """

    regionCode: str | None
    """Код региона РФ (ParticipantInfo@Rgn, 2 цифры)."""

    postalIndex: str | None
    """Почтовый индекс (ParticipantInfo@Ind)."""

    localityType: str | None
    """Тип населённого пункта (ParticipantInfo@Tnp, например "г", "пгт")."""

    locality: str | None
    """Наименование населённого пункта (ParticipantInfo@Nnp)."""

    address: str | None
    """Адрес участника (ParticipantInfo@Adr)."""

    registrationNumber: str | None
    """Регистрационный номер кредитной организации по КГРКО (ParticipantInfo@RegN). Есть не у всех."""

    uid: str | None
    """Уникальный идентификатор участника в справочнике (ParticipantInfo@UID). Сквозной ключ ЦБ."""

    dateIn: str | None
    """Дата включения участника в справочник (ParticipantInfo@DateIn). null, если не указана."""

    swift: str | None
    """
    «Основной» SWIFT/BIC-код участника (помеченный DefaultSWBIC="1", иначе первый из списка) —
    Полный список кодов — в swiftCodes. null, если код не задан.
    """

    swiftCodes: list[str]
    """
    Все SWIFT/BIC-коды участника (атрибуты SWBIC всех элементов <SWBICS>). У части участников
    их несколько (например, разные коды для подразделений). Пустой список, если SWIFT не задан.
    """

    accounts: list[CbrAccount]
    """
    Все счета участника из блока <Accounts> с их реквизитами (номер, контрольный ключ,
    подразделение Банка России, статус, дата открытия). Обычно один корсчёт (CRSA), но бывает больше.
    """

    restrictions: list[CbrRestriction]
    """
    Ограничения, наложенные на участника (блок <RstrList>). Например, код "URRS" — отзыв
    лицензии. Пустой список — действующих ограничений нет. Важно для оценки благонадёжности банка.
    """

    participantType: str | None
    """
    Тип участника (ParticipantInfo@PtType). Двузначный код ЦБ: например "00" — головной банк,
    "10"/"20" — филиалы, "40" — РКЦ, "52" — УФК. Возвращается в исходном виде справочника.
    """

    serviceCode: str | None
    """
    Код участия в системах/услугах Банка России (ParticipantInfo@Srvcs). Технический код ЦБ,
    отражающий доступные участнику сервисы. Возвращается в исходном виде. null, если не указан.
    """

    exchangeType: str | None
    """
    Тип обмена электронными сообщениями с Банком России (ParticipantInfo@XchType). Технический
    код ЦБ. Возвращается в исходном виде. null, если не указан.
    """

    status: str | None
    """
    Статус участника (ParticipantInfo@ParticipantStatus): "PSAC" — действующий.
    Возвращается в исходном виде справочника — по нему действующие участники отличаются
    от исключённых.
    """


class CbrSearchResponse(TypedDict, total=False):
    """Ответ на поиск по справочнику БИК: найденные карточки участников и параметры запроса."""

    query: str
    """Исходная строка запроса (как её ввёл пользователь)."""

    results: list[CbrBankInfo]
    """Найденные участники справочника."""

    count: int
    """Количество элементов в results."""

    elapsedMs: int
    """Время выполнения поиска в миллисекундах."""


class CbrStatsResponse(TypedDict, total=False):
    """Сведения о справочнике БИК: объём и дата актуальности данных."""

    isReady: bool
    """Готов ли справочник отвечать на запросы."""

    totalEntries: int
    """Всего записей в справочнике."""

    withCorrAccount: int
    """Количество участников, имеющих корреспондентский счёт (CRSA)."""

    withSwift: int
    """Количество участников с заполненным SWIFT."""

    directoryDate: str | None
    """
    Дата, на которую актуален справочник (атрибут BusinessDay корня <ED807>).
    null, если справочник ещё не загружен.
    """

    loadedAtUtc: str | None
    """Момент (UTC) последнего обновления данных справочника."""


__all__ = [
    "ApiError",
    "CbrAccount",
    "CbrAccountRestriction",
    "CbrBankInfo",
    "CbrRestriction",
    "CbrSearchResponse",
    "CbrStatsResponse",
]
