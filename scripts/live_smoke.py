"""
Ручная проверка SDK против живого API: по одному запросу на каждый из 23 сервисов.

По умолчанию — только на публичном демо-ключе (ответы-моки, деньги не списываются).
Лимиты демо-режима равны лимитам пользователя, поэтому скрипт не повторяет запросы и
останавливается на первом 429. В CI по пушу не запускается.

Запуск:
    python scripts/live_smoke.py
    python scripts/live_smoke.py --allow-live-key   # с ATLORIUM_API_KEY — ТРАТИТ КРЕДИТЫ
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import atlorium
from atlorium import ApiResponse, Atlorium

PNG = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "white.png"

Check = Callable[[Atlorium], ApiResponse[Any]]

CHECKS: list[tuple[str, Check]] = [
    ("egrul.get", lambda c: c.egrul.with_raw_response.get("7707083893")),
    ("cbr.get", lambda c: c.cbr.with_raw_response.get("044525225")),
    ("swift.get", lambda c: c.swift.with_raw_response.get("SABRRUMM")),
    ("bin.lookup", lambda c: c.bin.with_raw_response.lookup("424242")),
    ("aml.screen", lambda c: c.aml.with_raw_response.screen("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", "TRX")),
    ("ipinfo.lookup", lambda c: c.ipinfo.with_raw_response.lookup("8.8.8.8")),
    ("gar.search", lambda c: c.gar.with_raw_response.search("Москва Тверская", limit=1)),
    ("addressstd.standardize", lambda c: c.addressstd.with_raw_response.standardize("Москва, Тверская 1")),
    ("phone.validate", lambda c: c.phone.with_raw_response.validate("+79161234567")),
    ("email.validate", lambda c: c.email.with_raw_response.validate("test@example.com")),
    ("ocr.recognize", lambda c: c.ocr.with_raw_response.recognize(PNG)),
    ("dns.lookup", lambda c: c.dns.with_raw_response.lookup("atlorium.com")),
    ("cidr.calculate", lambda c: c.cidr.with_raw_response.calculate("192.168.1.10", 24)),
    ("cron.evaluate", lambda c: c.cron.with_raw_response.evaluate("*/15 * * * *", take=3)),
    ("certificate.check", lambda c: c.certificate.with_raw_response.check("atlorium.com")),
    ("weather.get", lambda c: c.weather.with_raw_response.get(55.7558, 37.6173)),
    ("aichat.send", lambda c: c.aichat.with_raw_response.send("Привет")),
    ("geocodeforward.search", lambda c: c.geocodeforward.with_raw_response.search("Москва, Тверская 1", size=1)),
    ("geocodereverse.lookup", lambda c: c.geocodereverse.with_raw_response.lookup(55.7558, 37.6173)),
    ("testdata.generate", lambda c: c.testdata.with_raw_response.generate(count=2, seed=42)),
    ("urlcheck.check", lambda c: c.urlcheck.with_raw_response.check("https://example.com")),
    ("pagespeed.audit", lambda c: c.pagespeed.with_raw_response.audit("https://atlorium.com")),
    ("imagecheck.analyze", lambda c: c.imagecheck.with_raw_response.analyze(PNG)),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--allow-live-key", action="store_true", help="разрешить боевой ключ (тратит кредиты)")
    args = parser.parse_args()

    with Atlorium(max_retries=0) as client:
        if not client.is_sandbox and not args.allow_live_key:
            print("Задан боевой ATLORIUM_API_KEY. Запуск с ним тратит кредиты — добавьте --allow-live-key.")
            return 2

        failures = 0
        for name, check in CHECKS:
            try:
                raw = check(client)
            except atlorium.RateLimitError as error:
                print(f"STOP {name}: 429, повторить через {error.retry_after} с. Дальше не идём.")
                return 3
            except atlorium.AtloriumError as error:
                failures += 1
                print(f"FAIL {name}: {error}")
                continue
            kind = type(raw.data).__name__
            print(f"OK   {name}: HTTP {raw.status_code}, sandbox={raw.is_sandbox}, {kind}")

    print(f"\nИтого: {len(CHECKS) - failures} из {len(CHECKS)} успешно.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
