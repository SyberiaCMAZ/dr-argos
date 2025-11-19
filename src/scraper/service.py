from typing import Callable

from crawlee import Request
from crawlee.crawlers import ParselCrawler, PlaywrightCrawler
from browserforge.headers import HeaderGenerator
from src.argos.models import ArgosListing

header_gen = HeaderGenerator(browser="firefox")


def to_request(listing: ArgosListing) -> Request:
    return Request.from_url(
        url=listing.url,
        label=f"{listing.marketplace.name}.handler_init",
        user_data={"item": listing.model_dump()},
        # headers=header_gen.generate()
    )


class ScrapingService:
    def __init__(
        self,
        parsel_crawler_provider: Callable[..., ParselCrawler],
        playwright_crawler_provider: Callable[..., PlaywrightCrawler],
    ):
        self._parsel_crawler_provider = parsel_crawler_provider
        self._playwright_crawler_provider = playwright_crawler_provider

    async def hydrate_listings(
        self, listings: list[ArgosListing]
    ) -> list[ArgosListing]:
        # We split listing into correct crawler playwright/ parsel
        crawler = self._playwright_crawler_provider()
        requests = [to_request(listing) for listing in listings]
        await crawler.run(
            requests=requests,
        )
        data = await crawler.get_data()
        hydrated_listings = [ArgosListing(**listing) for listing in data.items]
        return hydrated_listings
