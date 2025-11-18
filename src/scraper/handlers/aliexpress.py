from crawlee.crawlers import PlaywrightCrawlingContext

from src.scraper.pages.aliexpress import AliexpressDetailsPage
from src.scraper.handlers.core import PlaywrightHandler


# To run this handler you need to use cellular proxies due to Aliexpress anti-bot measures.
# Use tools.onebound for the initial results, then this handler for additional data.
class AliexpressDetailsRoute(PlaywrightHandler):
    name: str = "aliexpress"
    page_class: type[AliexpressDetailsPage] = AliexpressDetailsPage

    async def handler_init(self, context: PlaywrightCrawlingContext) -> None:
        if await context.page.is_visible(
            '//iframe[contains(@src, "captcharecaptcha")]'
        ):
            context.request.no_retry = True
            raise RuntimeError("Captcha detected")
        await super().handler_init(context)
