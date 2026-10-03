# atlorium — official Python SDK

[![PyPI](https://img.shields.io/pypi/v/atlorium.svg)](https://pypi.org/project/atlorium/)
[![Python](https://img.shields.io/pypi/pyversions/atlorium.svg)](https://pypi.org/project/atlorium/)
[![CI](https://github.com/atlorium-api/atlorium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/atlorium-api/atlorium-python/actions/workflows/ci.yml)

Russian company registry (EGRUL/EGRIP), bank BIK and SWIFT lookup, FIAS/GAR addresses, geocoding, OCR, DNS,
SSL, weather, AI chat and a dozen more B2B APIs for the Russian market — **all 23 [Atlorium](https://atlorium.com)
services in one package**.

- **All 59 API methods**, sync and async clients.
- **Fully typed** from the OpenAPI specs: autocompletion and `mypy --strict` work out of the box.
- **Works instantly, no sign-up** — on a public sandbox key.
- Retries on 429/503 honouring `Retry-After`, a clear exception hierarchy.
- Single dependency: [`httpx`](https://www.python-httpx.org/). Python 3.10+.

Russian documentation (primary): [README.md](https://github.com/atlorium-api/atlorium-python/blob/main/README.md)

## Install

```bash
pip install atlorium
```

## Quick start

```python
from atlorium import Atlorium

client = Atlorium()  # no key — sandbox mode

card = client.egrul.get("7707083893")  # company by INN / OGRN
print(card["shortName"], card["status"])

bank = client.cbr.get("044525225")  # bank by BIK
print(bank["name"], bank["corrAccount"])
```

Without a key the client uses the **public sandbox key** `ak_sandbox_demo_mockdata_v1`. The API returns
realistic but generated data (mocks), so you can build and test an integration before paying. Responses are
**deterministic** — the same request always returns the same result, which makes stable tests easy. The only
exception is timestamp fields.

Sandbox request limits are the same as for a registered user
(details: [atlorium.com/pricing](https://atlorium.com/pricing)).

If no key is given either as an argument or via the `ATLORIUM_API_KEY` variable, the SDK emits an
`atlorium.AtloriumSandboxWarning`, so a key forgotten in production never silently turns into mocks. To choose
sandbox mode explicitly and without the warning, pass the sandbox key: `Atlorium(atlorium.SANDBOX_API_KEY)`.

## Production key

Get a key at [atlorium.com](https://atlorium.com) and pass it in one of two ways:

```python
client = Atlorium("ak_...")  # explicitly
# or the ATLORIUM_API_KEY environment variable — no code changes
```

`client.is_sandbox` tells which mode the client is in. The key never appears in `repr` or in exception
messages.

## Services

| Service | Resource | Methods | Examples in 6 languages |
|---|---|---|---|
| Russian company registry (EGRUL/EGRIP) | `client.egrul` | `get`, `search`, `get_excerpt` | [egrul-api-client](https://github.com/atlorium-api/egrul-api-client) |
| Bank BIK directory (Bank of Russia) | `client.cbr` | `get`, `search`, `get_stats` | [cbr-bik-api-client](https://github.com/atlorium-api/cbr-bik-api-client) |
| SWIFT/BIC | `client.swift` | `get`, `search`, `validate`, `get_stats` | [swift-bic-api-client](https://github.com/atlorium-api/swift-bic-api-client) |
| Card BIN lookup | `client.bin` | `lookup`, `validate` | [bin-lookup-api-client](https://github.com/atlorium-api/bin-lookup-api-client) |
| Crypto wallet AML screening | `client.aml` | `screen`, `validate` | [aml-crypto-screening-api-client](https://github.com/atlorium-api/aml-crypto-screening-api-client) |
| IP profile | `client.ipinfo` | `lookup` | [ip-geolocation-api-client](https://github.com/atlorium-api/ip-geolocation-api-client) |
| FIAS/GAR addresses | `client.gar` | `search`, `suggest`, `get_object`, `get_object_by_id`, `get_children`, `get_hierarchy`, `get_stats`, `list_regions`, `get_region_stats` | [gar-fias-address-api-client](https://github.com/atlorium-api/gar-fias-address-api-client) |
| Address standardization | `client.addressstd` | `standardize` | [address-standardization-api-client](https://github.com/atlorium-api/address-standardization-api-client) |
| Phone validation | `client.phone` | `validate` | [phone-validation-api-client](https://github.com/atlorium-api/phone-validation-api-client) |
| E-mail verification | `client.email` | `validate` | [email-verification-api-client](https://github.com/atlorium-api/email-verification-api-client) |
| Text recognition (OCR) | `client.ocr` | `recognize` | [image-ocr-api-client](https://github.com/atlorium-api/image-ocr-api-client) |
| DNS | `client.dns` | `lookup`, `check_propagation` | [dns-lookup-api-client](https://github.com/atlorium-api/dns-lookup-api-client) |
| CIDR calculator | `client.cidr` | `calculate`, `split`, `check`, `supernet` | [cidr-subnet-calculator-api-client](https://github.com/atlorium-api/cidr-subnet-calculator-api-client) |
| Cron expressions | `client.cron` | `evaluate`, `build` | [cron-expression-parser-api-client](https://github.com/atlorium-api/cron-expression-parser-api-client) |
| SSL certificate | `client.certificate` | `check`, `check_url`, `check_batch` | [ssl-certificate-check-api-client](https://github.com/atlorium-api/ssl-certificate-check-api-client) |
| Weather | `client.weather` | `get` | [weather-api-client](https://github.com/atlorium-api/weather-api-client) |
| AI chat | `client.aichat` | `send`, `get_session`, `delete_session`, `list_models` | [ai-chat-api-client](https://github.com/atlorium-api/ai-chat-api-client) |
| Forward geocoding | `client.geocodeforward` | `search`, `search_structured`, `search_batch`, `get_place`, `search_postcode` | [geocoding-api-client](https://github.com/atlorium-api/geocoding-api-client) |
| Reverse geocoding | `client.geocodereverse` | `lookup`, `nearby` | [reverse-geocoding-api-client](https://github.com/atlorium-api/reverse-geocoding-api-client) |
| Russian test data generator | `client.testdata` | `generate`, `generate_with_body`, `list_fields` | [test-data-generator-api-client](https://github.com/atlorium-api/test-data-generator-api-client) |
| URL reputation | `client.urlcheck` | `check`, `check_batch` | [url-reputation-api-client](https://github.com/atlorium-api/url-reputation-api-client) |
| Site audit (Core Web Vitals) | `client.pagespeed` | `audit`, `audit_batch` | [core-web-vitals-api-client](https://github.com/atlorium-api/core-web-vitals-api-client) |
| Image moderation | `client.imagecheck` | `analyze` | [image-moderation-api-client](https://github.com/atlorium-api/image-moderation-api-client) |

Every method has a docstring describing its parameters, so your IDE shows it as you type. Docstrings are in
Russian.

## Examples

```python
from atlorium import Atlorium
from atlorium.types.cron import CronTemplateType, DayOfWeek

client = Atlorium()

# Counterparties and banks
client.egrul.search("Сбербанк", limit=5)
pdf = client.egrul.get_excerpt("7707083893")  # bytes — official registry excerpt
client.cbr.search("Тинькофф")
client.swift.validate("SABRRUMMXXX")
client.bin.lookup("424242")
client.aml.screen("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", "TRX")

# Addresses and maps
client.gar.suggest("Москва Тверская")
client.addressstd.standardize("мск тверская 1", geocode=True)
client.geocodeforward.search("Казань, Баумана 1", size=1)
client.geocodereverse.lookup(55.7558, 37.6173, include_admin=True)
client.weather.get(55.7558, 37.6173)

# Contacts
client.phone.validate("+79161234567")
client.email.validate("info@example.com")
client.ipinfo.lookup("8.8.8.8")

# Images: a path, bytes or an open binary file — the SDK encodes it to Base64 itself
client.ocr.recognize("scan.png")
with open("photo.jpg", "rb") as photo:
    client.imagecheck.analyze(photo, include_web_search=True)

# Websites and infrastructure
client.dns.lookup("atlorium.com")
client.dns.check_propagation("atlorium.com", resolvers=["1.1.1.1", "8.8.8.8"])
client.certificate.check("atlorium.com")
client.urlcheck.check_batch(["https://example.com", "https://example.org"])
client.pagespeed.audit("https://atlorium.com", strategy="mobile")
client.cidr.calculate("192.168.1.10", 24)
client.cron.evaluate("*/15 * * * *", time_zone_id="Europe/Moscow", take=3)
client.cron.build(template=CronTemplateType.WEEKLY, time_of_day="09:30:00", week_days=[DayOfWeek.MONDAY])

# AI chat and test data
reply = client.aichat.send("Draft a reconciliation letter to a counterparty")
client.aichat.send("Shorter, please", session_id=reply["sessionId"])
client.testdata.generate(count=10, fields=["fullName", "innPerson", "snils"], seed=42)
csv_text = client.testdata.generate(count=10, format="csv")  # str
```

## Async client

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

## Errors

All exceptions derive from `atlorium.AtloriumError`:

| HTTP | Exception | When |
|---|---|---|
| 400 | `ValidationError` | invalid input format |
| 401 | `AuthenticationError` | the key is missing, expired or invalid |
| 402 | `InsufficientCreditsError` | not enough credits (`error.balance` — current balance) |
| 403 | `PermissionDeniedError` | the service is not included in your account terms (code `service_not_in_account_terms`) — to enable it, write to support@atlorium.com |
| 404 | `NotFoundError` | object not found |
| 429 | `RateLimitError` | request limit exceeded (`error.retry_after` — seconds until you may retry) |
| 503 | `ServiceUnavailableError` | the service is temporarily unavailable: an upstream data source failure or planned maintenance (codes `service_disabled`, `maintenance`; status page — https://atlorium.com/status). **You are not charged for such a response** |
| other 5xx | `ServerError` | server-side error |
| — | `APIConnectionError`, `APITimeoutError` | network, timeout |

`ServiceUnavailableError` is a subclass of `ServerError`, so `except atlorium.ServerError` catches any 5xx
response, 503 included. Every response error has `error.retry_after` — the `Retry-After` header value in
seconds, or `None` if the server did not send one.

```python
import atlorium

try:
    card = client.egrul.get("7707083893")
except atlorium.NotFoundError:
    ...  # not in the registry
except atlorium.RateLimitError as error:
    print("Retry in", error.retry_after, "s")
except atlorium.ServiceUnavailableError as error:
    print("Service temporarily unavailable, not charged:", error.error_code)
except atlorium.AtloriumError as error:
    print(error.status, error.error_code, error)
```

`error.error_code` is a stable machine-readable code (`not_found`, `insufficient_credits`, `rate_limited_client`,
`service_disabled` …) — branch on it. Error messages are in Russian.

## Retries and timeouts

- Requests are retried automatically on **429, 503 and network errors** — up to `max_retries` times (default 2)
  with exponential backoff. The `Retry-After` header is honoured; if the server asks to wait longer than two
  minutes, the SDK does not hang but immediately raises the exception for that status — `RateLimitError` for
  429, `ServiceUnavailableError` for 503 — with `error.retry_after` set.
- **503 during planned maintenance** (codes `service_disabled` and `maintenance`) is not retried: retrying a
  second later would not help, so the SDK raises `ServiceUnavailableError` right away. Other 503 responses (an
  upstream source temporarily unavailable) are retried as usual.
- **POST requests** (AI chat, OCR, AML screening, batch checks) are retried after a network error only when the
  connection was never established and the request definitely was not sent. After a timeout or a dropped
  connection they are not: the operation may have run on the server, and a retry would charge you twice.
- 400, 401, 402, 403 and 404 are never retried.
- The default timeout is 30 s. Heavier operations have their own minimum: `ocr.recognize` and `pagespeed.audit`
  120 s, `pagespeed.audit_batch` 600 s, `imagecheck.analyze` 60 s, `aichat.send` 660 s (11 minutes).
- **AI chat** returns the reply as a whole, and a detailed answer may take several minutes, hence the 11-minute
  timeout of `aichat.send`. Do not lower it without a reason: if the client drops the connection earlier, the
  model still finishes the reply and the request is charged as completed.

```python
client = Atlorium(timeout=60, max_retries=5)
client.pagespeed.audit("https://atlorium.com", timeout=300)  # for a single call
fast = client.with_options(max_retries=0)  # a copy with different settings
```

## Response metadata

A regular call returns the data. When you need the status and headers, call the same method through
`with_raw_response`:

```python
raw = client.testdata.with_raw_response.generate(count=5)
print(raw.status_code, raw.is_sandbox, raw.headers.get("X-Atlorium-Seed"))
data = raw.data
```

`raw.is_sandbox` relies on the `X-Atlorium-Sandbox` header. For fully local services (for example, the test
data generator) the sandbox key returns a real result, and the header may be absent.

## Types

Response models are `TypedDict`s — plain `dict`s, so new server fields never break your code.

```python
from atlorium.types.egrul import CompanyLookupResult


def inn_of(card: CompanyLookupResult) -> str | None:
    return card.get("inn")
```

## Custom HTTP client

```python
import httpx
from atlorium import Atlorium

client = Atlorium(http_client=httpx.Client(proxy="http://proxy.local:3128"))
```

The SDK does not close such a client — your code owns its lifecycle. A client created by the SDK itself is
closed via `client.close()` or `with Atlorium() as client:`.

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff check . && ruff format --check . && mypy
python scripts/fetch_specs.py   # refresh the OpenAPI specs
python scripts/generate.py      # regenerate types and resources
```

`scripts/live_smoke.py` is a manual check against the live API on the sandbox key (one request per service).

## License

[MIT](https://github.com/atlorium-api/atlorium-python/blob/main/LICENSE)
