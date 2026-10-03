"""
Классы ресурсов (обычно напрямую не нужны — используйте ``client.<сервис>``).

СГЕНЕРИРОВАНО scripts/generate.py — не редактировать руками.
"""

from .addressstd import AddressStdResource, AsyncAddressStdResource
from .aichat import AiChatResource, AsyncAiChatResource
from .aml import AmlResource, AsyncAmlResource
from .bin import AsyncBinResource, BinResource
from .cbr import AsyncCbrResource, CbrResource
from .certificate import AsyncCertificateResource, CertificateResource
from .cidr import AsyncCidrResource, CidrResource
from .cron import AsyncCronResource, CronResource
from .dns import AsyncDnsResource, DnsResource
from .egrul import AsyncEgrulResource, EgrulResource
from .email import AsyncEmailResource, EmailResource
from .gar import AsyncGarResource, GarResource
from .geocodeforward import AsyncGeocodeForwardResource, GeocodeForwardResource
from .geocodereverse import AsyncGeocodeReverseResource, GeocodeReverseResource
from .imagecheck import AsyncImageCheckResource, ImageCheckResource
from .ipinfo import AsyncIpInfoResource, IpInfoResource
from .ocr import AsyncOcrResource, OcrResource
from .pagespeed import AsyncPageSpeedResource, PageSpeedResource
from .phone import AsyncPhoneResource, PhoneResource
from .swift import AsyncSwiftResource, SwiftResource
from .testdata import AsyncTestDataResource, TestDataResource
from .urlcheck import AsyncUrlCheckResource, UrlCheckResource
from .weather import AsyncWeatherResource, WeatherResource

__all__ = [
    "AddressStdResource",
    "AiChatResource",
    "AmlResource",
    "AsyncAddressStdResource",
    "AsyncAiChatResource",
    "AsyncAmlResource",
    "AsyncBinResource",
    "AsyncCbrResource",
    "AsyncCertificateResource",
    "AsyncCidrResource",
    "AsyncCronResource",
    "AsyncDnsResource",
    "AsyncEgrulResource",
    "AsyncEmailResource",
    "AsyncGarResource",
    "AsyncGeocodeForwardResource",
    "AsyncGeocodeReverseResource",
    "AsyncImageCheckResource",
    "AsyncIpInfoResource",
    "AsyncOcrResource",
    "AsyncPageSpeedResource",
    "AsyncPhoneResource",
    "AsyncSwiftResource",
    "AsyncTestDataResource",
    "AsyncUrlCheckResource",
    "AsyncWeatherResource",
    "BinResource",
    "CbrResource",
    "CertificateResource",
    "CidrResource",
    "CronResource",
    "DnsResource",
    "EgrulResource",
    "EmailResource",
    "GarResource",
    "GeocodeForwardResource",
    "GeocodeReverseResource",
    "ImageCheckResource",
    "IpInfoResource",
    "OcrResource",
    "PageSpeedResource",
    "PhoneResource",
    "SwiftResource",
    "TestDataResource",
    "UrlCheckResource",
    "WeatherResource",
]
