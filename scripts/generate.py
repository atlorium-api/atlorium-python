"""
Генератор типов и ресурсов SDK из OpenAPI-спек ``spec/<id>_ru.json``.

Что создаётся (всё — перезаписывается при каждом запуске, руками не редактировать):

* ``src/atlorium/types/<id>.py`` — ``TypedDict`` и ``Literal`` для всех схем сервиса;
* ``src/atlorium/resources/<id>.py`` — синхронный и асинхронный ресурс плюс обёртки
  ``with_raw_response``;
* ``src/atlorium/_resources_mixin.py`` — свойства ``client.<id>``.

Таблица :data:`OPERATIONS` — единая для всех SDK Atlorium: имена методов, обязательные
параметры (в спеках query-параметры не помечены обязательными, поэтому они перечислены
здесь явно) и особые случаи. Скрипт падает, если в спеке есть операция без записи в
таблице или в таблице есть операция, которой нет в спеке.

Все файлы пишутся в UTF-8 с переводом строки LF на любой ОС, поэтому повторный запуск на
тех же спеках не меняет ни одного файла.

Запуск (после ``python scripts/fetch_specs.py``, если спеки обновились):
    python scripts/generate.py
"""

from __future__ import annotations

import json
import keyword
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = ROOT / "spec"
PACKAGE_DIR = ROOT / "src" / "atlorium"
TYPES_DIR = PACKAGE_DIR / "types"
RESOURCES_DIR = PACKAGE_DIR / "resources"

GENERATED_NOTE = "СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками."

JsonObject = dict[str, Any]


@dataclass(frozen=True)
class Service:
    id: str
    class_prefix: str
    repo: str


SERVICES: list[Service] = [
    Service("egrul", "Egrul", "egrul-api-client"),
    Service("cbr", "Cbr", "cbr-bik-api-client"),
    Service("swift", "Swift", "swift-bic-api-client"),
    Service("bin", "Bin", "bin-lookup-api-client"),
    Service("aml", "Aml", "aml-crypto-screening-api-client"),
    Service("ipinfo", "IpInfo", "ip-geolocation-api-client"),
    Service("gar", "Gar", "gar-fias-address-api-client"),
    Service("addressstd", "AddressStd", "address-standardization-api-client"),
    Service("phone", "Phone", "phone-validation-api-client"),
    Service("email", "Email", "email-verification-api-client"),
    Service("ocr", "Ocr", "image-ocr-api-client"),
    Service("dns", "Dns", "dns-lookup-api-client"),
    Service("cidr", "Cidr", "cidr-subnet-calculator-api-client"),
    Service("cron", "Cron", "cron-expression-parser-api-client"),
    Service("certificate", "Certificate", "ssl-certificate-check-api-client"),
    Service("weather", "Weather", "weather-api-client"),
    Service("aichat", "AiChat", "ai-chat-api-client"),
    Service("geocodeforward", "GeocodeForward", "geocoding-api-client"),
    Service("geocodereverse", "GeocodeReverse", "reverse-geocoding-api-client"),
    Service("testdata", "TestData", "test-data-generator-api-client"),
    Service("urlcheck", "UrlCheck", "url-reputation-api-client"),
    Service("pagespeed", "PageSpeed", "core-web-vitals-api-client"),
    Service("imagecheck", "ImageCheck", "image-moderation-api-client"),
]


@dataclass(frozen=True)
class Operation:
    service: str
    http: str
    path: str
    """Маршрут точно как в спеке (регистр важен только для сопоставления со спекой)."""
    name: str
    required: tuple[str, ...] = ()
    """Обязательные query/body-параметры (имена API) — по фактическому поведению сервера."""
    list_params: tuple[str, ...] = ()
    """Query-параметры-списки: принимают строку или последовательность, склеиваются запятой."""
    image_params: tuple[str, ...] = ()
    """Поля тела с изображением: путь/байты/поток, SDK кодирует в Base64."""
    body_name: str | None = None
    """Имя аргумента для тела-массива (у спеки у такого тела имени нет)."""
    default_timeout: float | None = None
    csv_overload: bool = False
    """Параметр ``format``: ``"csv"`` возвращает строку, иначе JSON."""
    skip_description: bool = False
    """Не брать description операции в docstring (пример в нём расходится с сервером)."""


OPERATIONS: list[Operation] = [
    Operation("egrul", "GET", "/api/Egrul/{query}", "get"),
    Operation("egrul", "GET", "/api/Egrul/search", "search", required=("query",)),
    Operation("egrul", "GET", "/api/Egrul/{query}/excerpt", "get_excerpt"),
    Operation("cbr", "GET", "/api/Cbr/{bik}", "get"),
    Operation("cbr", "GET", "/api/Cbr/search", "search", required=("query",)),
    Operation("cbr", "GET", "/api/Cbr/stats", "get_stats"),
    Operation("swift", "GET", "/api/Swift/{bic}", "get"),
    Operation("swift", "GET", "/api/Swift/search", "search", required=("query",)),
    Operation("swift", "GET", "/api/Swift/validate/{bic}", "validate"),
    Operation("swift", "GET", "/api/Swift/stats", "get_stats"),
    Operation("bin", "GET", "/api/Bin/{bin}", "lookup"),
    Operation("bin", "GET", "/api/Bin/validate/{bin}", "validate"),
    Operation("aml", "POST", "/api/Aml/screen", "screen", required=("walletAddress", "blockchain")),
    Operation("aml", "GET", "/api/Aml/validate", "validate", required=("walletAddress", "blockchain")),
    Operation("ipinfo", "GET", "/api/IpInfo/{ip}", "lookup"),
    Operation("gar", "GET", "/api/Gar/search", "search", required=("query",)),
    Operation("gar", "GET", "/api/Gar/suggest", "suggest", required=("query",)),
    Operation("gar", "GET", "/api/Gar/object/{guid}", "get_object"),
    Operation("gar", "GET", "/api/Gar/object/id/{objectId}", "get_object_by_id"),
    Operation("gar", "GET", "/api/Gar/children/{parentObjectId}", "get_children"),
    Operation("gar", "GET", "/api/Gar/hierarchy/{objectId}", "get_hierarchy"),
    Operation("gar", "GET", "/api/Gar/stats", "get_stats"),
    Operation("gar", "GET", "/api/Gar/regions", "list_regions"),
    Operation("gar", "GET", "/api/Gar/region/{regionCode}/stats", "get_region_stats"),
    Operation("addressstd", "GET", "/api/AddressStd", "standardize", required=("address",)),
    Operation("phone", "GET", "/api/Phone/{number}", "validate"),
    Operation("email", "GET", "/api/EmailValidation", "validate", required=("email",)),
    Operation(
        "ocr",
        "POST",
        "/api/Ocr/image-to-text",
        "recognize",
        required=("image",),
        image_params=("image",),
        default_timeout=120,
    ),
    Operation("dns", "GET", "/api/Dns/lookup", "lookup", required=("domain",)),
    Operation(
        "dns", "GET", "/api/Dns/propagation", "check_propagation", required=("domain",), list_params=("resolvers",)
    ),
    Operation("cidr", "GET", "/api/Cidr/calculate", "calculate", required=("ip", "mask")),
    Operation("cidr", "GET", "/api/Cidr/subnets", "split", required=("cidr", "newMask")),
    Operation("cidr", "GET", "/api/Cidr/check", "check", required=("cidr", "ip")),
    Operation("cidr", "POST", "/api/Cidr/supernet", "supernet", required=("inputs",)),
    Operation("cron", "POST", "/api/Cron/evaluate", "evaluate", required=("expression",)),
    Operation("cron", "POST", "/api/Cron/build", "build", skip_description=True),
    Operation("certificate", "GET", "/api/Certificate", "check", required=("host",)),
    Operation("certificate", "GET", "/api/Certificate/url", "check_url", required=("url",)),
    Operation(
        "certificate", "GET", "/api/Certificate/batch", "check_batch", required=("hosts",), list_params=("hosts",)
    ),
    Operation("weather", "GET", "/api/Weather", "get", required=("latitude", "longitude")),
    Operation("aichat", "POST", "/api/AiChat/send", "send", required=("message",), default_timeout=660),
    Operation("aichat", "GET", "/api/AiChat/session/{sessionId}", "get_session"),
    Operation("aichat", "DELETE", "/api/AiChat/session/{sessionId}", "delete_session"),
    Operation("aichat", "GET", "/api/AiChat/models", "list_models"),
    Operation("geocodeforward", "GET", "/api/geocodeforward", "search", required=("text",)),
    Operation("geocodeforward", "GET", "/api/geocodeforward/structured", "search_structured"),
    Operation("geocodeforward", "POST", "/api/geocodeforward/batch", "search_batch", required=("queries",)),
    Operation("geocodeforward", "GET", "/api/geocodeforward/place", "get_place", required=("placeId",)),
    Operation("geocodeforward", "GET", "/api/geocodeforward/postcode", "search_postcode", required=("code",)),
    Operation("geocodereverse", "GET", "/api/geocodereverse", "lookup", required=("lat", "lon")),
    Operation("geocodereverse", "GET", "/api/geocodereverse/nearby", "nearby", required=("lat", "lon")),
    Operation("testdata", "GET", "/api/TestData", "generate", list_params=("fields",), csv_overload=True),
    Operation("testdata", "POST", "/api/TestData", "generate_with_body", list_params=("fields",), csv_overload=True),
    Operation("testdata", "GET", "/api/TestData/fields", "list_fields"),
    Operation("urlcheck", "GET", "/api/urlcheck", "check", required=("url",)),
    Operation("urlcheck", "POST", "/api/urlcheck/batch", "check_batch", required=("urls",), body_name="urls"),
    Operation("pagespeed", "GET", "/api/pagespeed", "audit", required=("url",), default_timeout=120),
    Operation(
        "pagespeed",
        "POST",
        "/api/pagespeed/batch",
        "audit_batch",
        required=("urls",),
        body_name="urls",
        default_timeout=600,
    ),
    Operation(
        "imagecheck",
        "POST",
        "/api/imagecheck",
        "analyze",
        required=("image",),
        image_params=("image",),
        default_timeout=60,
    ),
]

NULLABLE_OVERRIDES: dict[str, set[str]] = {
    # Поля-объекты, которые спека описывает ненулевыми, а сервер может отдать null.
    "swift": {"headquarters"},
    "ipinfo": {"asn", "company", "flags", "carrier", "privacy", "abuse", "hostedDomains", "abuseReports"},
    "addressstd": {"gar", "geo"},
    "weather": {"rain", "snow"},
    "pagespeed": {"fieldData"},
    "imagecheck": {"webSearch"},
}

INT_ENUMS: dict[str, list[tuple[str, int, str]]] = {
    # В спеке это голый integer без enum; значения — по документации сервиса.
    "CronTemplateType": [
        ("EVERY_MINUTE", 0, "Каждую минуту."),
        ("EVERY_N_MINUTES", 1, "Каждые N минут (шаг — ``interval``)."),
        ("HOURLY", 2, "Раз в час, в начале часа."),
        ("EVERY_N_HOURS", 3, "Каждые N часов (шаг — ``interval``)."),
        ("DAILY", 4, "Раз в сутки, в ``time_of_day``."),
        ("WEEKLY", 5, "В выбранные дни недели (``week_days``), в ``time_of_day``."),
        ("MONTHLY", 6, "Раз в месяц: число ``day_of_month``, время ``time_of_day``."),
    ],
    "DayOfWeek": [
        ("SUNDAY", 0, "Воскресенье."),
        ("MONDAY", 1, "Понедельник."),
        ("TUESDAY", 2, "Вторник."),
        ("WEDNESDAY", 3, "Среда."),
        ("THURSDAY", 4, "Четверг."),
        ("FRIDAY", 5, "Пятница."),
        ("SATURDAY", 6, "Суббота."),
    ],
}

TYPE_NAMES_RESERVED = {"Any", "Literal", "TypedDict", "IntEnum"}


# ── Утилиты ─────────────────────────────────────────────────────────────────────


def snake_case(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[1]


def docstring(text: str, indent: str) -> str:
    """Текст как docstring: экранирует обратные слэши и тройные кавычки."""
    text = text.strip().replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if text.endswith('"'):
        text = text[:-1] + '\\"'
    lines = [line.rstrip() for line in text.splitlines()]
    if len(lines) == 1:
        return f'{indent}"""{lines[0]}"""\n'
    body = "\n".join(indent + line if line else "" for line in lines)
    return f'{indent}"""\n{body}\n{indent}"""\n'


def load_spec(service_id: str) -> JsonObject:
    with (SPEC_DIR / f"{service_id}_ru.json").open(encoding="utf-8") as file:
        spec: JsonObject = json.load(file)
    return spec


def schema_refs(schema: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(schema, dict):
        ref = schema.get("$ref")
        if isinstance(ref, str):
            found.add(ref_name(ref))
        for value in schema.values():
            found |= schema_refs(value)
    elif isinstance(schema, list):
        for item in schema:
            found |= schema_refs(item)
    return found


# ── Типы ────────────────────────────────────────────────────────────────────────


class TypeRenderer:
    """Переводит JSON-схему в аннотацию Python."""

    def __init__(self, schemas: dict[str, JsonObject], prefix: str) -> None:
        self.schemas = schemas
        self.prefix = prefix

    def named(self, name: str) -> str:
        if name in INT_ENUMS:
            return "int"
        return self.prefix + name

    def render(self, schema: JsonObject) -> tuple[str, bool]:
        """Возвращает (аннотация без None, допускает ли схема null)."""
        ref = schema.get("$ref")
        if isinstance(ref, str):
            return self.named(ref_name(ref)), False
        all_of = schema.get("allOf")
        if isinstance(all_of, list) and len(all_of) == 1:
            return self.render(all_of[0])
        for key in ("oneOf", "anyOf"):
            variants = schema.get(key)
            if isinstance(variants, list):
                parts: list[str] = []
                nullable = False
                for variant in variants:
                    if variant.get("type") == "null":
                        nullable = True
                        continue
                    expr, variant_nullable = self.render(variant)
                    nullable = nullable or variant_nullable
                    parts.append(expr)
                return (" | ".join(dict.fromkeys(parts)) or "Any"), nullable
        enum = schema.get("enum")
        if isinstance(enum, list):
            return "Literal[" + ", ".join(json.dumps(value, ensure_ascii=False) for value in enum) + "]", False

        raw_type = schema.get("type")
        types = raw_type if isinstance(raw_type, list) else ([raw_type] if raw_type else [])
        nullable = "null" in types
        types = [kind for kind in types if kind != "null"]
        if not types and ("properties" in schema or "additionalProperties" in schema):
            types = ["object"]
        if not types:
            return "Any", nullable
        # ["integer","string"]: на входе сервер принимает и строку, а в ответах всегда пишет число.
        if "integer" in types:
            return "int", nullable
        if "number" in types:
            return "float", nullable
        if types == ["string"]:
            return "str", nullable
        if types == ["boolean"]:
            return "bool", nullable
        if types == ["array"]:
            item, item_nullable = self.render(schema.get("items", {}))
            return f"list[{with_none(item, item_nullable)}]", nullable
        if types == ["object"]:
            extra = schema.get("additionalProperties")
            if isinstance(extra, dict):
                value, value_nullable = self.render(extra)
                return f"dict[str, {with_none(value, value_nullable)}]", nullable
            return "dict[str, Any]", nullable
        return "Any", nullable


def with_none(expr: str, nullable: bool) -> str:
    return f"{expr} | None" if nullable and expr != "Any" else expr


def sorted_schema_names(schemas: dict[str, JsonObject]) -> list[str]:
    """Топологический порядок: зависимости раньше зависимых (нужно функциональным TypedDict)."""
    ordered: list[str] = []
    state: dict[str, int] = {}

    def visit(name: str) -> None:
        if state.get(name) == 2 or name not in schemas:
            return
        if state.get(name) == 1:
            return  # цикл: с `from __future__ import annotations` в классах это не страшно
        state[name] = 1
        for dep in sorted(schema_refs(schemas[name])):
            visit(dep)
        state[name] = 2
        ordered.append(name)

    for name in sorted(schemas):
        visit(name)
    return ordered


def generate_types(service: Service, spec: JsonObject) -> str:
    schemas: dict[str, JsonObject] = spec.get("components", {}).get("schemas", {})
    reserved = TYPE_NAMES_RESERVED & set(schemas)
    if reserved:
        raise SystemExit(f"{service.id}: имена схем конфликтуют с импортами: {reserved}")
    renderer = TypeRenderer(schemas, prefix="")
    overrides = NULLABLE_OVERRIDES.get(service.id, set())
    title = spec.get("info", {}).get("title", service.id)

    out: list[str] = [
        f'"""\nТипы запросов и ответов сервиса «{title}».\n\n'
        f"Модели ответов — ``TypedDict`` (обычные ``dict``): новые поля сервера не ломают разбор.\n\n"
        f'{GENERATED_NOTE} Источник: spec/{service.id}_ru.json.\n"""\n\n',
        "from __future__ import annotations\n\n",
        "from enum import IntEnum\n",
        "from typing import Any, Literal, TypedDict\n\n",
    ]
    exported: list[str] = []

    for name in sorted_schema_names(schemas):
        schema = schemas[name]
        description = str(schema.get("description") or "").strip()
        exported.append(name)
        out.append("\n")
        if name in INT_ENUMS:
            out.append(f"class {name}(IntEnum):\n")
            out.append(docstring(description or name, "    "))
            for member, value, comment in INT_ENUMS[name]:
                out.append(f"\n    {member} = {value}\n")
                out.append(docstring(comment, "    "))
            continue

        properties: dict[str, JsonObject] | None = schema.get("properties")
        if not isinstance(properties, dict):
            expr, _ = renderer.render(schema)
            out.append(f"{name} = {expr}\n")
            if description:
                out.append(docstring(description, ""))
            continue

        fields: list[tuple[str, str, str]] = []
        for prop_name, prop in properties.items():
            expr, nullable = renderer.render(prop)
            expr = with_none(expr, nullable or prop_name in overrides)
            fields.append((prop_name, expr, str(prop.get("description") or "").strip()))

        if all(key.isidentifier() and not keyword.iskeyword(key) for key, _, _ in fields):
            out.append(f"class {name}(TypedDict, total=False):\n")
            out.append(docstring(description or name, "    "))
            for key, expr, field_doc in fields:
                out.append(f"\n    {key}: {expr}\n")
                if field_doc:
                    out.append(docstring(field_doc, "    "))
        else:
            # Ключи, недопустимые как идентификаторы (например, «1h» у осадков), — функциональный синтаксис.
            items = ", ".join(f"{json.dumps(key)}: {json.dumps(expr)}" for key, expr, _ in fields)
            out.append(f"{name} = TypedDict({json.dumps(name)}, {{{items}}}, total=False)\n")
            docs = [f"``{key}``: {field_doc}" for key, _, field_doc in fields if field_doc]
            out.append(docstring("\n\n".join(filter(None, [description, *docs])) or name, ""))

    out.append("\n__all__ = [" + ", ".join(json.dumps(name) for name in sorted(exported)) + "]\n")
    return "".join(out)


# ── Ресурсы ─────────────────────────────────────────────────────────────────────


@dataclass
class Param:
    api: str
    py: str
    location: str  # path | query | body | body_array
    required: bool
    annotation: str
    description: str

    @property
    def value_expr(self) -> str:
        if self.annotation == "FileInput":
            return f"encode_image({self.py})"
        if self.annotation in ("str | Sequence[str]", "Sequence[str]"):
            # Строка — тоже Sequence[str]; ensure_sequence не даст разбить её на символы.
            return self.none_guard(f"ensure_sequence({self.py})")
        if self.annotation.startswith("Sequence["):
            return self.none_guard(f"list({self.py})")
        return self.py

    def none_guard(self, expr: str) -> str:
        return expr if self.required else f"None if {self.py} is None else {expr}"

    @property
    def full_annotation(self) -> str:
        return self.annotation if self.required else f"{self.annotation} | None"


def param_annotation(op: Operation, api_name: str, schema: JsonObject, renderer: TypeRenderer) -> str:
    if api_name in op.image_params:
        return "FileInput"
    if api_name in op.list_params:
        return "str | Sequence[str]"
    if op.csv_overload and api_name == "format":
        return 'Literal["json", "csv"]'
    if schema.get("format") == "date-time":
        return "datetime | str"
    raw_type = schema.get("type")
    types = raw_type if isinstance(raw_type, list) else [raw_type]
    if "array" in types:
        item, _ = renderer.render(schema.get("items", {}))
        return f"Sequence[{item}]"
    expr, _ = renderer.render(schema)
    return expr


def collect_params(op: Operation, spec_op: JsonObject, schemas: dict[str, JsonObject]) -> list[Param]:
    renderer = TypeRenderer(schemas, prefix="_types.")
    params: list[Param] = []
    for raw in spec_op.get("parameters", []):
        location = raw["in"]
        if location not in ("path", "query"):
            raise SystemExit(f"{op.service}.{op.name}: параметр в {location} не поддерживается")
        name = raw["name"]
        params.append(
            Param(
                api=name,
                py=snake_case(name),
                location=location,
                required=location == "path" or name in op.required,
                annotation=param_annotation(op, name, raw.get("schema", {}), renderer),
                description=str(raw.get("description") or "").strip(),
            )
        )

    body = spec_op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if isinstance(body, dict):
        if "$ref" in body:
            body_schema = schemas[ref_name(body["$ref"])]
            for name, prop in body_schema.get("properties", {}).items():
                params.append(
                    Param(
                        api=name,
                        py=snake_case(name),
                        location="body",
                        required=name in op.required,
                        annotation=param_annotation(op, name, prop, renderer),
                        description=str(prop.get("description") or "").strip(),
                    )
                )
        elif body.get("type") == "array":
            if not op.body_name:
                raise SystemExit(f"{op.service}.{op.name}: тело-массив без body_name")
            item, _ = renderer.render(body.get("items", {}))
            params.append(
                Param(
                    api=op.body_name,
                    py=snake_case(op.body_name),
                    location="body_array",
                    required=True,
                    annotation=f"Sequence[{item}]",
                    description=str(spec_op["requestBody"].get("description") or "Список значений.").strip(),
                )
            )
        else:
            raise SystemExit(f"{op.service}.{op.name}: неизвестная форма тела {body}")

    known = {param.api for param in params}
    missing = set(op.required) - known
    if missing:
        raise SystemExit(f"{op.service}.{op.name}: обязательные параметры не найдены в спеке: {missing}")
    names = [param.py for param in params]
    if len(names) != len(set(names)) or "timeout" in names or any(keyword.iskeyword(n) for n in names):
        raise SystemExit(f"{op.service}.{op.name}: конфликт имён параметров {names}")
    return params


def response_info(op: Operation, spec_op: JsonObject, schemas: dict[str, JsonObject]) -> tuple[str, str]:
    """(аннотация результата, response_type транспорта)."""
    content: JsonObject = spec_op.get("responses", {}).get("200", {}).get("content", {})
    if "application/pdf" in content:
        return "bytes", "bytes"
    schema = (content.get("application/json") or {}).get("schema")
    if not isinstance(schema, dict):
        return "None", "json"
    if schema.get("type") == "string":
        # Сервер отдаёт строку JSON-строкой или простым текстом — в зависимости от Accept.
        return "str", "auto"
    expr, _ = TypeRenderer(schemas, prefix="_types.").render(schema)
    if op.csv_overload:
        return expr, "auto"
    return expr, "json"


def positional_and_keyword(params: list[Param], op: Operation) -> tuple[list[Param], list[Param]]:
    path = [p for p in params if p.location == "path"]
    required_order = {name: index for index, name in enumerate(op.required)}
    required = sorted(
        (p for p in params if p.location != "path" and p.required), key=lambda p: required_order.get(p.api, 99)
    )
    optional = [p for p in params if not p.required]
    return path + required, optional


def render_path(op: Operation) -> str:
    parts = re.split(r"(\{[^}]+\})", op.path)
    rendered: list[str] = []
    has_params = False
    for part in parts:
        if part.startswith("{"):
            rendered.append("{path_segment(" + snake_case(part[1:-1]) + ")}")
            has_params = True
        else:
            rendered.append(part.lower())
    literal = "".join(rendered)
    return f'f"{literal}"' if has_params else f'"{literal}"'


def signature(
    positional: list[Param], keyword_only: list[Param], *, format_override: str | None = None, self_arg: bool = True
) -> str:
    parts = ["self"] if self_arg else []
    parts += [f"{p.py}: {p.annotation}" for p in positional]
    parts.append("*")
    for p in keyword_only:
        if format_override is not None and p.api == "format":
            parts.append(f"format: {format_override}")
        else:
            parts.append(f"{p.py}: {p.annotation} | None = None")
    parts.append("timeout: float | None = None")
    return ", ".join(parts)


def method_doc(op: Operation, spec_op: JsonObject, params: list[Param], returns: str) -> str:
    summary = str(spec_op.get("summary") or "").strip()
    description = "" if op.skip_description else str(spec_op.get("description") or "").strip()
    lines = [summary or op.name]
    if description and description != summary:
        lines += ["", description]
    lines += ["", "Аргументы:"]
    for param in params:
        text = param.description.replace("\n", " ").strip() or "—"
        lines.append(f"    {param.py}: {text}")
    lines.append("    timeout: таймаут этого вызова в секундах (перекрывает настройки клиента).")
    if returns == "bytes":
        lines += ["", "Возвращает содержимое файла (``bytes``)."]
    if op.csv_overload:
        lines += ["", 'При ``format="csv"`` возвращает строку CSV, иначе — разобранный JSON.']
    return "\n".join(lines)


def generate_resource(service: Service, spec: JsonObject) -> tuple[str, int]:
    schemas: dict[str, JsonObject] = spec.get("components", {}).get("schemas", {})
    ops = [op for op in OPERATIONS if op.service == service.id]
    spec_ops = {
        (method.upper(), path): body
        for path, methods in spec["paths"].items()
        for method, body in methods.items()
        if method in ("get", "post", "put", "delete", "patch")
    }
    table_keys = {(op.http, op.path) for op in ops}
    if set(spec_ops) != table_keys:
        raise SystemExit(
            f"{service.id}: таблица операций не совпадает со спекой.\n"
            f"  нет в таблице: {sorted(set(spec_ops) - table_keys)}\n"
            f"  нет в спеке: {sorted(table_keys - set(spec_ops))}"
        )

    title = spec.get("info", {}).get("title", service.id)
    sync_cls = f"{service.class_prefix}Resource"
    async_cls = f"Async{service.class_prefix}Resource"
    builders: list[str] = []
    sync_methods: list[str] = []
    async_methods: list[str] = []
    sync_raw: list[str] = []
    async_raw: list[str] = []

    for op in ops:
        spec_op = spec_ops[(op.http, op.path)]
        params = collect_params(op, spec_op, schemas)
        positional, keyword_only = positional_and_keyword(params, op)
        returns, response_type = response_info(op, spec_op, schemas)
        builder = f"_{op.name}_options"

        # Построитель RequestOptions — общий для sync и async.
        builder_args = ", ".join([f"{p.py}: {p.full_annotation}" for p in params] + ["timeout: float | None"])
        query = [p for p in params if p.location in ("path", "query") and p.location != "path"]
        body = [p for p in params if p.location == "body"]
        body_array = [p for p in params if p.location == "body_array"]
        options = [f'method="{op.http}"', f"path={render_path(op)}"]
        if query:
            options.append("params={" + ", ".join(f'"{p.api}": {p.value_expr}' for p in query) + "}")
        if body:
            options.append("json=strip_none({" + ", ".join(f'"{p.api}": {p.value_expr}' for p in body) + "})")
            options.append("has_body=True")
        elif body_array:
            options.append(f"json={body_array[0].value_expr}")
            options.append("has_body=True")
        elif op.http == "POST":
            options.append("has_body=True")
        options.append("timeout=timeout")
        if op.default_timeout is not None:
            options.append(f"default_timeout={op.default_timeout:g}")
        if response_type != "json":
            options.append(f'response_type="{response_type}"')
        builders.append(
            f"def {builder}(*, {builder_args}) -> RequestOptions:\n    return RequestOptions({', '.join(options)})\n"
        )

        call_args = ", ".join([f"{p.py}={p.py}" for p in params] + ["timeout=timeout"])
        doc = docstring(method_doc(op, spec_op, params, returns), "        ")
        full_returns = f"{returns} | str" if op.csv_overload else returns
        base_sig = signature(positional, keyword_only)

        if op.csv_overload:
            json_sig = signature(positional, keyword_only, format_override='Literal["json"] | None = None')
            csv_sig = signature(positional, keyword_only, format_override='Literal["csv"]')
            for kind, methods in (("sync", sync_methods), ("async", async_methods)):
                prefix = "async def" if kind == "async" else "def"
                methods.append(f"    @overload\n    {prefix} {op.name}({json_sig}) -> {returns}: ...\n")
                methods.append(f"    @overload\n    {prefix} {op.name}({csv_sig}) -> str: ...\n")

        sync_methods.append(
            f"    def {op.name}({base_sig}) -> {full_returns}:\n{doc}"
            f'        return cast("{full_returns}", self._client.request({builder}({call_args})))\n'
        )
        async_methods.append(
            f"    async def {op.name}({base_sig}) -> {full_returns}:\n{doc}"
            f'        return cast("{full_returns}", await self._client.request({builder}({call_args})))\n'
        )
        if op.csv_overload:
            sync_raw.append(
                f"        self.{op.name} = to_raw_response_wrapper(\n"
                f'            cast("Callable[..., {full_returns}]", resource.{op.name})\n        )\n'
            )
            async_raw.append(
                f"        self.{op.name} = to_async_raw_response_wrapper(\n"
                f'            cast("Callable[..., Awaitable[{full_returns}]]", resource.{op.name})\n        )\n'
            )
        else:
            sync_raw.append(f"        self.{op.name} = to_raw_response_wrapper(resource.{op.name})\n")
            async_raw.append(f"        self.{op.name} = to_async_raw_response_wrapper(resource.{op.name})\n")

    link = f"https://github.com/atlorium-api/{service.repo}"
    class_doc = f"{title}.\n\nПримеры на шести языках: {link}"
    raw_doc = (
        "Те же методы, но каждый возвращает :class:`~atlorium.ApiResponse`: данные вместе со статусом и заголовками."
    )
    needs_overload = any(op.csv_overload for op in ops)

    out: list[str] = [
        f'"""\nРесурс «{title}»: ``client.{service.id}``.\n\n{GENERATED_NOTE}\n"""\n\n',
        "from __future__ import annotations\n\n",
        "from collections.abc import Sequence\n",
        "from datetime import datetime\n",
        "from functools import cached_property\n",
        f"from typing import {'TYPE_CHECKING, ' if needs_overload else ''}Literal, cast, overload\n\n",
        "from .._base_client import RequestOptions, ensure_sequence, path_segment\n",
        "from .._files import FileInput, encode_image\n",
        "from .._resource import AsyncAPIResource, SyncAPIResource, strip_none\n",
        "from .._response import to_async_raw_response_wrapper, to_raw_response_wrapper\n",
        f"from ..types import {service.id} as _types\n\n",
    ]
    if needs_overload:
        out.append("if TYPE_CHECKING:\n    from collections.abc import Awaitable, Callable\n\n")
    out.append(f'__all__ = ["{async_cls}", "{sync_cls}"]\n\n\n')
    out.append("\n\n".join(builders))
    for cls, base, methods, raw_cls in (
        (sync_cls, "SyncAPIResource", sync_methods, f"{sync_cls}WithRawResponse"),
        (async_cls, "AsyncAPIResource", async_methods, f"{async_cls}WithRawResponse"),
    ):
        out.append(f"\n\nclass {cls}({base}):\n")
        out.append(docstring(class_doc, "    "))
        out.append(
            f"\n    @cached_property\n    def with_raw_response(self) -> {raw_cls}:\n"
            f"{docstring(raw_doc, '        ')}"
            f"        return {raw_cls}(self)\n"
        )
        out.append("\n" + "\n".join(methods))
    for raw_cls, cls, lines in (
        (f"{sync_cls}WithRawResponse", sync_cls, sync_raw),
        (f"{async_cls}WithRawResponse", async_cls, async_raw),
    ):
        out.append(f"\n\nclass {raw_cls}:\n")
        out.append(docstring(f"Методы :class:`{cls}`, возвращающие :class:`~atlorium.ApiResponse`.", "    "))
        out.append(f"\n    def __init__(self, resource: {cls}) -> None:\n" + "".join(lines))
    return "".join(out), len(ops)


def generate_mixin(titles: dict[str, str]) -> str:
    out = [
        f'"""\nРесурсы клиентов: ``client.egrul``, ``client.cbr`` и т.д.\n\n{GENERATED_NOTE}\n"""\n\n',
        "from __future__ import annotations\n\n",
        "from functools import cached_property\n",
        "from typing import TYPE_CHECKING, cast\n\n",
    ]
    for service in SERVICES:
        out.append(
            f"from .resources.{service.id} import Async{service.class_prefix}Resource, {service.class_prefix}Resource\n"
        )
    out.append("\nif TYPE_CHECKING:\n    from ._base_client import AsyncAPIClient, SyncAPIClient\n\n")
    out.append('__all__ = ["AsyncResourcesMixin", "SyncResourcesMixin"]\n\n')
    for kind in ("Sync", "Async"):
        prefix = "Async" if kind == "Async" else ""
        out.append(f"\nclass {kind}ResourcesMixin:\n")
        flavour = "асинхронного" if prefix else "синхронного"
        out.append(docstring(f"Сервисы Atlorium как свойства {flavour} клиента.", "    "))
        for service in SERVICES:
            cls = f"{prefix}{service.class_prefix}Resource"
            out.append(
                f"\n    @cached_property\n    def {service.id}(self) -> {cls}:\n"
                f"{docstring(titles[service.id], '        ')}"
                f'        return {cls}(cast("{kind}APIClient", self))\n'
            )
    return "".join(out)


def generate_package_inits() -> tuple[str, str]:
    ids = [service.id for service in SERVICES]
    types_init = (
        '"""\nТипы запросов и ответов по сервисам: ``atlorium.types.egrul.CompanyLookupResult`` и т.д.\n\n'
        f'{GENERATED_NOTE}\n"""\n\n'
        f"from . import {', '.join(sorted(ids))}\n\n"
        "__all__ = [" + ", ".join(json.dumps(i) for i in sorted(ids)) + "]\n"
    )
    names: list[str] = []
    lines: list[str] = []
    for service in SERVICES:
        pair = [f"Async{service.class_prefix}Resource", f"{service.class_prefix}Resource"]
        names += pair
        lines.append(f"from .{service.id} import {', '.join(pair)}\n")
    resources_init = (
        '"""\nКлассы ресурсов (обычно напрямую не нужны — используйте ``client.<сервис>``).\n\n'
        + f'{GENERATED_NOTE}\n"""\n\n'
        + "".join(lines)
        + "\n__all__ = ["
        + ", ".join(json.dumps(n) for n in sorted(names))
        + "]\n"
    )
    return types_init, resources_init


def write_file(path: Path, text: str) -> None:
    """UTF-8 и LF на любой ОС: вывод генератора не зависит от платформы."""
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def run_ruff(paths: list[Path]) -> None:
    targets = [str(path) for path in paths]
    python = sys.executable
    subprocess.run([python, "-m", "ruff", "check", "--fix", "--quiet", *targets], check=False)  # noqa: S603
    subprocess.run([python, "-m", "ruff", "format", "--quiet", *targets], check=True)  # noqa: S603


def main() -> int:
    table_services = {op.service for op in OPERATIONS}
    known_services = {service.id for service in SERVICES}
    if table_services != known_services:
        raise SystemExit(f"Сервисы таблицы и списка расходятся: {table_services ^ known_services}")

    for directory in (TYPES_DIR, RESOURCES_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True)

    titles: dict[str, str] = {}
    total = 0
    for service in SERVICES:
        spec = load_spec(service.id)
        titles[service.id] = str(spec.get("info", {}).get("title", service.id))
        write_file(TYPES_DIR / f"{service.id}.py", generate_types(service, spec))
        code, count = generate_resource(service, spec)
        write_file(RESOURCES_DIR / f"{service.id}.py", code)
        total += count

    types_init, resources_init = generate_package_inits()
    write_file(TYPES_DIR / "__init__.py", types_init)
    write_file(RESOURCES_DIR / "__init__.py", resources_init)
    mixin = PACKAGE_DIR / "_resources_mixin.py"
    write_file(mixin, generate_mixin(titles))

    run_ruff([TYPES_DIR, RESOURCES_DIR, mixin])
    print(f"Сгенерировано: {len(SERVICES)} сервисов, {total} операций.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
