"""
Ресурсы клиентов: ``client.egrul``, ``client.cbr`` и т.д.

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

from .resources.addressstd import AddressStdResource, AsyncAddressStdResource
from .resources.aichat import AiChatResource, AsyncAiChatResource
from .resources.aml import AmlResource, AsyncAmlResource
from .resources.bin import AsyncBinResource, BinResource
from .resources.cbr import AsyncCbrResource, CbrResource
from .resources.certificate import AsyncCertificateResource, CertificateResource
from .resources.cidr import AsyncCidrResource, CidrResource
from .resources.cron import AsyncCronResource, CronResource
from .resources.dns import AsyncDnsResource, DnsResource
from .resources.egrul import AsyncEgrulResource, EgrulResource
from .resources.email import AsyncEmailResource, EmailResource
from .resources.gar import AsyncGarResource, GarResource
from .resources.geocodeforward import AsyncGeocodeForwardResource, GeocodeForwardResource
from .resources.geocodereverse import AsyncGeocodeReverseResource, GeocodeReverseResource
from .resources.imagecheck import AsyncImageCheckResource, ImageCheckResource
from .resources.ipinfo import AsyncIpInfoResource, IpInfoResource
from .resources.ocr import AsyncOcrResource, OcrResource
from .resources.pagespeed import AsyncPageSpeedResource, PageSpeedResource
from .resources.phone import AsyncPhoneResource, PhoneResource
from .resources.swift import AsyncSwiftResource, SwiftResource
from .resources.testdata import AsyncTestDataResource, TestDataResource
from .resources.urlcheck import AsyncUrlCheckResource, UrlCheckResource
from .resources.weather import AsyncWeatherResource, WeatherResource

if TYPE_CHECKING:
    from ._base_client import AsyncAPIClient, SyncAPIClient

__all__ = ["AsyncResourcesMixin", "SyncResourcesMixin"]


class SyncResourcesMixin:
    """Сервисы Atlorium как свойства синхронного клиента."""

    @cached_property
    def egrul(self) -> EgrulResource:
        """API ЕГРЮЛ/ЕГРИП"""
        return EgrulResource(cast("SyncAPIClient", self))

    @cached_property
    def cbr(self) -> CbrResource:
        """API справочника БИК"""
        return CbrResource(cast("SyncAPIClient", self))

    @cached_property
    def swift(self) -> SwiftResource:
        """API справочника SWIFT/BIC"""
        return SwiftResource(cast("SyncAPIClient", self))

    @cached_property
    def bin(self) -> BinResource:
        """API BIN Lookup"""
        return BinResource(cast("SyncAPIClient", self))

    @cached_property
    def aml(self) -> AmlResource:
        """API AML-скоринга"""
        return AmlResource(cast("SyncAPIClient", self))

    @cached_property
    def ipinfo(self) -> IpInfoResource:
        """API профиля IP"""
        return IpInfoResource(cast("SyncAPIClient", self))

    @cached_property
    def gar(self) -> GarResource:
        """ГАР/ФИАС API"""
        return GarResource(cast("SyncAPIClient", self))

    @cached_property
    def addressstd(self) -> AddressStdResource:
        """API стандартизации адреса"""
        return AddressStdResource(cast("SyncAPIClient", self))

    @cached_property
    def phone(self) -> PhoneResource:
        """API валидации телефона"""
        return PhoneResource(cast("SyncAPIClient", self))

    @cached_property
    def email(self) -> EmailResource:
        """API проверки почты"""
        return EmailResource(cast("SyncAPIClient", self))

    @cached_property
    def ocr(self) -> OcrResource:
        """API распознавания текста с изображения"""
        return OcrResource(cast("SyncAPIClient", self))

    @cached_property
    def dns(self) -> DnsResource:
        """API проверки DNS"""
        return DnsResource(cast("SyncAPIClient", self))

    @cached_property
    def cidr(self) -> CidrResource:
        """API калькулятора подсетей"""
        return CidrResource(cast("SyncAPIClient", self))

    @cached_property
    def cron(self) -> CronResource:
        """API разбора Cron-выражений"""
        return CronResource(cast("SyncAPIClient", self))

    @cached_property
    def certificate(self) -> CertificateResource:
        """API проверки SSL-сертификата"""
        return CertificateResource(cast("SyncAPIClient", self))

    @cached_property
    def weather(self) -> WeatherResource:
        """API погодных данных"""
        return WeatherResource(cast("SyncAPIClient", self))

    @cached_property
    def aichat(self) -> AiChatResource:
        """API ИИ-чата"""
        return AiChatResource(cast("SyncAPIClient", self))

    @cached_property
    def geocodeforward(self) -> GeocodeForwardResource:
        """API прямого геокодинга"""
        return GeocodeForwardResource(cast("SyncAPIClient", self))

    @cached_property
    def geocodereverse(self) -> GeocodeReverseResource:
        """API обратного геокодинга"""
        return GeocodeReverseResource(cast("SyncAPIClient", self))

    @cached_property
    def testdata(self) -> TestDataResource:
        """API генератора тестовых данных РФ"""
        return TestDataResource(cast("SyncAPIClient", self))

    @cached_property
    def urlcheck(self) -> UrlCheckResource:
        """API проверки ссылки"""
        return UrlCheckResource(cast("SyncAPIClient", self))

    @cached_property
    def pagespeed(self) -> PageSpeedResource:
        """API аудита сайта"""
        return PageSpeedResource(cast("SyncAPIClient", self))

    @cached_property
    def imagecheck(self) -> ImageCheckResource:
        """API анализа изображения"""
        return ImageCheckResource(cast("SyncAPIClient", self))


class AsyncResourcesMixin:
    """Сервисы Atlorium как свойства асинхронного клиента."""

    @cached_property
    def egrul(self) -> AsyncEgrulResource:
        """API ЕГРЮЛ/ЕГРИП"""
        return AsyncEgrulResource(cast("AsyncAPIClient", self))

    @cached_property
    def cbr(self) -> AsyncCbrResource:
        """API справочника БИК"""
        return AsyncCbrResource(cast("AsyncAPIClient", self))

    @cached_property
    def swift(self) -> AsyncSwiftResource:
        """API справочника SWIFT/BIC"""
        return AsyncSwiftResource(cast("AsyncAPIClient", self))

    @cached_property
    def bin(self) -> AsyncBinResource:
        """API BIN Lookup"""
        return AsyncBinResource(cast("AsyncAPIClient", self))

    @cached_property
    def aml(self) -> AsyncAmlResource:
        """API AML-скоринга"""
        return AsyncAmlResource(cast("AsyncAPIClient", self))

    @cached_property
    def ipinfo(self) -> AsyncIpInfoResource:
        """API профиля IP"""
        return AsyncIpInfoResource(cast("AsyncAPIClient", self))

    @cached_property
    def gar(self) -> AsyncGarResource:
        """ГАР/ФИАС API"""
        return AsyncGarResource(cast("AsyncAPIClient", self))

    @cached_property
    def addressstd(self) -> AsyncAddressStdResource:
        """API стандартизации адреса"""
        return AsyncAddressStdResource(cast("AsyncAPIClient", self))

    @cached_property
    def phone(self) -> AsyncPhoneResource:
        """API валидации телефона"""
        return AsyncPhoneResource(cast("AsyncAPIClient", self))

    @cached_property
    def email(self) -> AsyncEmailResource:
        """API проверки почты"""
        return AsyncEmailResource(cast("AsyncAPIClient", self))

    @cached_property
    def ocr(self) -> AsyncOcrResource:
        """API распознавания текста с изображения"""
        return AsyncOcrResource(cast("AsyncAPIClient", self))

    @cached_property
    def dns(self) -> AsyncDnsResource:
        """API проверки DNS"""
        return AsyncDnsResource(cast("AsyncAPIClient", self))

    @cached_property
    def cidr(self) -> AsyncCidrResource:
        """API калькулятора подсетей"""
        return AsyncCidrResource(cast("AsyncAPIClient", self))

    @cached_property
    def cron(self) -> AsyncCronResource:
        """API разбора Cron-выражений"""
        return AsyncCronResource(cast("AsyncAPIClient", self))

    @cached_property
    def certificate(self) -> AsyncCertificateResource:
        """API проверки SSL-сертификата"""
        return AsyncCertificateResource(cast("AsyncAPIClient", self))

    @cached_property
    def weather(self) -> AsyncWeatherResource:
        """API погодных данных"""
        return AsyncWeatherResource(cast("AsyncAPIClient", self))

    @cached_property
    def aichat(self) -> AsyncAiChatResource:
        """API ИИ-чата"""
        return AsyncAiChatResource(cast("AsyncAPIClient", self))

    @cached_property
    def geocodeforward(self) -> AsyncGeocodeForwardResource:
        """API прямого геокодинга"""
        return AsyncGeocodeForwardResource(cast("AsyncAPIClient", self))

    @cached_property
    def geocodereverse(self) -> AsyncGeocodeReverseResource:
        """API обратного геокодинга"""
        return AsyncGeocodeReverseResource(cast("AsyncAPIClient", self))

    @cached_property
    def testdata(self) -> AsyncTestDataResource:
        """API генератора тестовых данных РФ"""
        return AsyncTestDataResource(cast("AsyncAPIClient", self))

    @cached_property
    def urlcheck(self) -> AsyncUrlCheckResource:
        """API проверки ссылки"""
        return AsyncUrlCheckResource(cast("AsyncAPIClient", self))

    @cached_property
    def pagespeed(self) -> AsyncPageSpeedResource:
        """API аудита сайта"""
        return AsyncPageSpeedResource(cast("AsyncAPIClient", self))

    @cached_property
    def imagecheck(self) -> AsyncImageCheckResource:
        """API анализа изображения"""
        return AsyncImageCheckResource(cast("AsyncAPIClient", self))
