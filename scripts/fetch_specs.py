"""
Скачивает живые OpenAPI-спеки всех 23 сервисов Atlorium в каталог ``spec/``.

Спеки коммитятся в репозиторий, чтобы генерация типов и ресурсов (``scripts/generate.py``)
была воспроизводимой без сети. Файлы пишутся всегда одинаково — UTF-8, отступ 2, перевод
строки LF на любой ОС, — поэтому повторное скачивание неизменных спек не меняет файлов.

Запуск:
    python scripts/fetch_specs.py
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://atlorium.com/openapi"
SPEC_IDS = [
    "egrul",
    "cbr",
    "swift",
    "bin",
    "aml",
    "ipinfo",
    "gar",
    "addressstd",
    "phone",
    "email",
    "ocr",
    "dns",
    "cidr",
    "cron",
    "certificate",
    "weather",
    "aichat",
    "geocodeforward",
    "geocodereverse",
    "testdata",
    "urlcheck",
    "pagespeed",
    "imagecheck",
]
LOCALES = ["ru", "en-US"]
SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"


def write_spec(target: Path, data: object) -> None:
    """Записывает спеку в каноническом виде (единственное место, где задан формат файлов ``spec/``)."""
    with target.open("w", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    SPEC_DIR.mkdir(exist_ok=True)
    failed = 0
    for spec_id in SPEC_IDS:
        for locale in LOCALES:
            url = f"{BASE_URL}/{spec_id}_{locale}.json"
            request = urllib.request.Request(url, headers={"User-Agent": "atlorium-python-specfetch"})
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    data = json.loads(response.read().decode("utf-8"))
            except Exception as error:
                print(f"[!] {url}: {error}", file=sys.stderr)
                failed += 1
                continue
            target = SPEC_DIR / f"{spec_id}_{locale}.json"
            write_spec(target, data)
            print(f"ok  {target.name}")
            time.sleep(0.2)  # небольшая пауза между запросами, чтобы не создавать лишнюю нагрузку
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
