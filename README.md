# atlorium — официальный Python SDK

[![PyPI](https://img.shields.io/pypi/v/atlorium.svg)](https://pypi.org/project/atlorium/)
[![Python](https://img.shields.io/pypi/pyversions/atlorium.svg)](https://pypi.org/project/atlorium/)
[![CI](https://github.com/atlorium-api/atlorium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/atlorium-api/atlorium-python/actions/workflows/ci.yml)

Проверка контрагентов по ЕГРЮЛ, БИК и SWIFT, адреса ГАР/ФИАС, геокодинг, OCR, DNS, SSL,
погода, ИИ-чат и ещё десяток B2B API для российского рынка — **23 сервиса [Atlorium](https://atlorium.com)
в одном пакете**.

- **Все 59 методов API**, синхронный и асинхронный клиент.
- **Полная типизация**: параметры и ответы описаны по OpenAPI-спекам, работает автодополнение и `mypy --strict`.
- **Работает сразу, без регистрации** — на публичном демо-ключе.
- Ретраи на 429/503 с учётом `Retry-After`, понятные исключения на русском.
- Одна зависимость — [`httpx`](https://www.python-httpx.org/). Python 3.10+.

English: [README.en.md](https://github.com/atlorium-api/atlorium-python/blob/main/README.en.md)

## Установка

```bash
pip install atlorium
```

## Быстрый старт

```python
from atlorium import Atlorium

client = Atlorium()  # без ключа — демо-режим

card = client.egrul.get("7707083893")
print(card["shortName"], card["status"])

bank = client.cbr.get("044525225")
print(bank["name"], bank["corrAccount"])
```

Без ключа клиент работает на **публичном демо-ключе** `ak_sandbox_demo_mockdata_v1`. API отвечает
правдоподобными, но сгенерированными данными (моками): можно встроить и проверить интеграцию до
оплаты. Ответы **детерминированы** — один и тот же запрос всегда даёт один и тот же результат,
поэтому на них удобно писать стабильные тесты. Исключение — поля-отметки времени.

Лимиты запросов в демо-режиме такие же, как у зарегистрированного пользователя
(подробности — [atlorium.com/pricing](https://atlorium.com/pricing)).

Если ключ не задан ни аргументом, ни переменной `ATLORIUM_API_KEY`, SDK выдаёт предупреждение `atlorium.AtloriumSandboxWarning`:
так забытый в проде ключ не превратится в тихую работу на моках. Чтобы выбрать демо-режим явно и без
предупреждения, передайте демо-ключ: `Atlorium(atlorium.SANDBOX_API_KEY)`.

## Боевой ключ

Получите ключ на [atlorium.com](https://atlorium.com) и передайте его одним из способов:

```python
client = Atlorium("ak_...")  # явно
# или переменная окружения ATLORIUM_API_KEY — код не меняется
```

`client.is_sandbox` показывает, в каком режиме работает клиент. Ключ не попадает ни в `repr`,
ни в тексты исключений.

## Сервисы

| Сервис | Ресурс | Методы | Примеры на 6 языках |
|---|---|---|---|
| ЕГРЮЛ/ЕГРИП | `client.egrul` | `get`, `search`, `get_excerpt` | [egrul-api-client](https://github.com/atlorium-api/egrul-api-client) |
| Справочник БИК ЦБ РФ | `client.cbr` | `get`, `search`, `get_stats` | [cbr-bik-api-client](https://github.com/atlorium-api/cbr-bik-api-client) |
| SWIFT/BIC | `client.swift` | `get`, `search`, `validate`, `get_stats` | [swift-bic-api-client](https://github.com/atlorium-api/swift-bic-api-client) |
| BIN банковской карты | `client.bin` | `lookup`, `validate` | [bin-lookup-api-client](https://github.com/atlorium-api/bin-lookup-api-client) |
| AML-скоринг криптокошелька | `client.aml` | `screen`, `validate` | [aml-crypto-screening-api-client](https://github.com/atlorium-api/aml-crypto-screening-api-client) |
| Профиль IP | `client.ipinfo` | `lookup` | [ip-geolocation-api-client](https://github.com/atlorium-api/ip-geolocation-api-client) |
| Адреса ГАР/ФИАС | `client.gar` | `search`, `suggest`, `get_object`, `get_object_by_id`, `get_children`, `get_hierarchy`, `get_stats`, `list_regions`, `get_region_stats` | [gar-fias-address-api-client](https://github.com/atlorium-api/gar-fias-address-api-client) |
| Стандартизация адреса | `client.addressstd` | `standardize` | [address-standardization-api-client](https://github.com/atlorium-api/address-standardization-api-client) |
| Валидация телефона | `client.phone` | `validate` | [phone-validation-api-client](https://github.com/atlorium-api/phone-validation-api-client) |
| Проверка e-mail | `client.email` | `validate` | [email-verification-api-client](https://github.com/atlorium-api/email-verification-api-client) |
| Распознавание текста (OCR) | `client.ocr` | `recognize` | [image-ocr-api-client](https://github.com/atlorium-api/image-ocr-api-client) |
| DNS | `client.dns` | `lookup`, `check_propagation` | [dns-lookup-api-client](https://github.com/atlorium-api/dns-lookup-api-client) |
| CIDR-калькулятор | `client.cidr` | `calculate`, `split`, `check`, `supernet` | [cidr-subnet-calculator-api-client](https://github.com/atlorium-api/cidr-subnet-calculator-api-client) |
| Cron-выражения | `client.cron` | `evaluate`, `build` | [cron-expression-parser-api-client](https://github.com/atlorium-api/cron-expression-parser-api-client) |
| SSL-сертификат | `client.certificate` | `check`, `check_url`, `check_batch` | [ssl-certificate-check-api-client](https://github.com/atlorium-api/ssl-certificate-check-api-client) |
| Погода | `client.weather` | `get` | [weather-api-client](https://github.com/atlorium-api/weather-api-client) |
| ИИ-чат | `client.aichat` | `send`, `get_session`, `delete_session`, `list_models` | [ai-chat-api-client](https://github.com/atlorium-api/ai-chat-api-client) |
| Прямой геокодинг | `client.geocodeforward` | `search`, `search_structured`, `search_batch`, `get_place`, `search_postcode` | [geocoding-api-client](https://github.com/atlorium-api/geocoding-api-client) |
| Обратный геокодинг | `client.geocodereverse` | `lookup`, `nearby` | [reverse-geocoding-api-client](https://github.com/atlorium-api/reverse-geocoding-api-client) |
| Генератор тестовых данных РФ | `client.testdata` | `generate`, `generate_with_body`, `list_fields` | [test-data-generator-api-client](https://github.com/atlorium-api/test-data-generator-api-client) |
| Проверка ссылки | `client.urlcheck` | `check`, `check_batch` | [url-reputation-api-client](https://github.com/atlorium-api/url-reputation-api-client) |
| Аудит сайта (Core Web Vitals) | `client.pagespeed` | `audit`, `audit_batch` | [core-web-vitals-api-client](https://github.com/atlorium-api/core-web-vitals-api-client) |
| Модерация изображений | `client.imagecheck` | `analyze` | [image-moderation-api-client](https://github.com/atlorium-api/image-moderation-api-client) |

У каждого метода docstring с описанием параметров — IDE покажет его при наборе.

## Примеры

```python
from atlorium import Atlorium
from atlorium.types.cron import CronTemplateType, DayOfWeek

client = Atlorium()

# Контрагенты и банки
client.egrul.search("Сбербанк", limit=5)
pdf = client.egrul.get_excerpt("7707083893")  # bytes — официальная выписка
client.cbr.search("Тинькофф")
client.swift.validate("SABRRUMMXXX")
client.bin.lookup("424242")
client.aml.screen("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", "TRX")

# Адреса и карты
client.gar.suggest("Москва Тверская")
client.addressstd.standardize("мск тверская 1", geocode=True)
client.geocodeforward.search("Казань, Баумана 1", size=1)
client.geocodereverse.lookup(55.7558, 37.6173, include_admin=True)
client.weather.get(55.7558, 37.6173)

# Контакты
client.phone.validate("+79161234567")
client.email.validate("info@example.com")
client.ipinfo.lookup("8.8.8.8")

# Изображения: путь, bytes или открытый бинарный файл — SDK сам кодирует в Base64
client.ocr.recognize("scan.png")
with open("photo.jpg", "rb") as photo:
    client.imagecheck.analyze(photo, include_web_search=True)

# Сайты и инфраструктура
client.dns.lookup("atlorium.com")
client.dns.check_propagation("atlorium.com", resolvers=["1.1.1.1", "8.8.8.8"])
client.certificate.check("atlorium.com")
client.urlcheck.check_batch(["https://example.com", "https://example.org"])
client.pagespeed.audit("https://atlorium.com", strategy="mobile")
client.cidr.calculate("192.168.1.10", 24)
client.cron.evaluate("*/15 * * * *", time_zone_id="Europe/Moscow", take=3)
client.cron.build(template=CronTemplateType.WEEKLY, time_of_day="09:30:00", week_days=[DayOfWeek.MONDAY])

# ИИ-чат и тестовые данные
reply = client.aichat.send("Составь письмо контрагенту о сверке")
client.aichat.send("Короче", session_id=reply["sessionId"])
client.testdata.generate(count=10, fields=["fullName", "innPerson", "snils"], seed=42)
csv_text = client.testdata.generate(count=10, format="csv")  # str
```

## Асинхронный клиент

```python
import asyncio
from atlorium import AsyncAtlorium


async def main() -> None:
    async with AsyncAtlorium() as client:
        card, bank = await asyncio.gather(
            client.egrul.get("7707083893"),
            client.cbr.get("044525225"),
        )


asyncio.run(main())
```

## Ошибки

Все исключения наследуются от `atlorium.AtloriumError`:

| HTTP | Исключение | Когда |
|---|---|---|
| 400 | `ValidationError` | неверный формат входных данных |
| 401 | `AuthenticationError` | ключ отсутствует, просрочен или недействителен |
| 402 | `InsufficientCreditsError` | недостаточно кредитов (`error.balance` — текущий баланс) |
| 403 | `PermissionDeniedError` | сервис не входит в условия вашей учётной записи (код `service_not_in_account_terms`) — чтобы подключить его, напишите на support@atlorium.com |
| 404 | `NotFoundError` | объект не найден |
| 429 | `RateLimitError` | превышен лимит запросов (`error.retry_after` — через сколько секунд повторить) |
| 503 | `ServiceUnavailableError` | сервис временно недоступен: сбой внешнего источника данных или плановые работы (коды `service_disabled`, `maintenance`; состояние — https://atlorium.com/status). **Деньги за такой ответ не списываются** |
| прочие 5xx | `ServerError` | ошибка на стороне сервера |
| — | `APIConnectionError`, `APITimeoutError` | сеть, таймаут |

`ServiceUnavailableError` — подкласс `ServerError`, поэтому `except atlorium.ServerError` ловит любой ответ
5xx, включая 503. У каждой ошибки ответа есть `error.retry_after` — значение заголовка `Retry-After`
в секундах или `None`, если сервер его не прислал.

```python
import atlorium

try:
    card = client.egrul.get("7707083893")
except atlorium.NotFoundError:
    ...  # нет в реестре
except atlorium.RateLimitError as error:
    print("Повторить через", error.retry_after, "с")
except atlorium.ServiceUnavailableError as error:
    print("Сервис временно недоступен, деньги не списаны:", error.error_code)
except atlorium.AtloriumError as error:
    print(error.status, error.error_code, error)
```

`error.error_code` — стабильный машинный код (`not_found`, `insufficient_credits`, `rate_limited_client`,
`service_disabled` …), по нему и стоит ветвиться.

## Ретраи и таймауты

- Запрос автоматически повторяется на **429, 503 и сетевых ошибках** — до `max_retries` раз (по умолчанию 2)
  с экспоненциальной задержкой. Заголовок `Retry-After` учитывается; если сервер просит ждать дольше
  двух минут, SDK не висит, а сразу бросает исключение этого статуса — `RateLimitError` для 429,
  `ServiceUnavailableError` для 503 — с `error.retry_after`.
- **503 при плановых работах** (коды `service_disabled` и `maintenance`) не повторяется: повтор через
  секунду ничего не даст, SDK сразу бросает `ServiceUnavailableError`. Прочие 503 (внешний источник
  временно недоступен) повторяются как обычно.
- **POST-запросы** (ИИ-чат, OCR, AML-скрининг, пакетные проверки) после сетевой ошибки повторяются, только
  если соединение не установилось и запрос точно не ушёл. После таймаута или обрыва соединения — нет:
  операция могла выполниться на сервере, и повтор списал бы деньги второй раз.
- 400, 401, 402, 403 и 404 не повторяются никогда.
- Таймаут по умолчанию — 30 с. Для тяжёлых операций свой минимум: `ocr.recognize` и `pagespeed.audit` — 120 с,
  `pagespeed.audit_batch` — 600 с, `imagecheck.analyze` — 60 с, `aichat.send` — 660 с (11 минут).
- **ИИ-чат** отвечает целиком, а развёрнутый ответ модели может готовиться несколько минут, поэтому
  у `aichat.send` таймаут 11 минут. Не уменьшайте его без необходимости: если клиент оборвёт соединение
  раньше, модель всё равно допишет ответ, и запрос будет оплачен как выполненный.

```python
client = Atlorium(timeout=60, max_retries=5)
client.pagespeed.audit("https://atlorium.com", timeout=300)  # на один вызов
fast = client.with_options(max_retries=0)  # копия с другими настройками
```

## Метаданные ответа

Обычный вызов возвращает данные. Нужны статус и заголовки — вызовите тот же метод через
`with_raw_response`:

```python
raw = client.testdata.with_raw_response.generate(count=5)
print(raw.status_code, raw.is_sandbox, raw.headers.get("X-Atlorium-Seed"))
data = raw.data
```

`raw.is_sandbox` опирается на заголовок `X-Atlorium-Sandbox`. У полностью локальных сервисов (например,
генератора тестовых данных) демо-ключ возвращает настоящий результат, и заголовка может не быть.

## Типы

Модели ответов — `TypedDict`, то есть обычные `dict`: новые поля на сервере не ломают код.

```python
from atlorium.types.egrul import CompanyLookupResult


def inn_of(card: CompanyLookupResult) -> str | None:
    return card.get("inn")
```

## Свой HTTP-клиент

```python
import httpx
from atlorium import Atlorium

client = Atlorium(http_client=httpx.Client(proxy="http://proxy.local:3128"))
```

Такой клиент SDK не закрывает — жизненным циклом управляет ваш код. Созданный самим SDK клиент
закрывается через `client.close()` или `with Atlorium() as client:`.

## Разработка

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff check . && ruff format --check . && mypy
python scripts/fetch_specs.py   # обновить OpenAPI-спеки
python scripts/generate.py      # перегенерировать типы и ресурсы
```

`scripts/live_smoke.py` — ручная проверка против живого API на демо-ключе (по одному запросу на сервис).

## Лицензия

[MIT](https://github.com/atlorium-api/atlorium-python/blob/main/LICENSE)
