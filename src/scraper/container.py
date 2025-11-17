from typing import Any

from crawlee.crawlers import ParselCrawler, PlaywrightCrawler
from crawlee.http_clients import ImpitHttpClient
from crawlee.proxy_configuration import ProxyConfiguration
from crawlee.storage_clients import MemoryStorageClient
from dependency_injector import containers, providers

from src.scraper.service import ScrapingService
from src.scraper.handlers.core import AutoRouter, discover_handlers


def create_parsel_crawler(router: AutoRouter[Any]) -> ParselCrawler:
    return


class ScrapingContainer(containers.DeclarativeContainer):
    handlers_registry = providers.Resource(discover_handlers, "src.scraper.handlers")
    router = providers.Singleton(AutoRouter, handlers_registry)
    proxy_configuration = providers.Singleton(
        ProxyConfiguration,
        proxy_urls=[],
    )
    playwright_crawler = providers.Factory(
        PlaywrightCrawler,
        request_handler=router,
        browser_type="firefox",
        headless=False,
        storage_client=providers.Factory(MemoryStorageClient),
        # proxy_configuration=proxy_configuration,
    )
    _http_client = providers.Singleton(ImpitHttpClient)
    parsel_crawler = providers.Factory(
        ParselCrawler,
        http_client=_http_client,
        storage_client=MemoryStorageClient(),
        request_handler=router,
        # proxy_configuration=proxy_configuration,
    )
    scraping_service = providers.Singleton(
        ScrapingService,
        parsel_crawler_provider=parsel_crawler.provider,
        playwright_crawler_provider=playwright_crawler.provider,
    )
