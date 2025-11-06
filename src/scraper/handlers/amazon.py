from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext

from src.scraper.pages.amazon import AmazonDetailsPage
from src.scraper.handlers.core import PlaywrightHandler
from urllib.parse import urlparse


class AmazonDetailsRoute(PlaywrightHandler):
    name: str = "amazon"
    page_class: type[AmazonDetailsPage] = AmazonDetailsPage

    async def handler_init_not_used(self, context: ParselCrawlingContext) -> None:
        parsed_url = urlparse(context.request.url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        csrf_token = context.selector.xpath(
            '//input[@name="anti-csrftoken-a2z"]/@value'
        ).extract_first()
        response = await context.send_request(
            url=domain + "/portal-migration/hz/glow/address-change?actionSource=glow",
            headers={
                **context.request.headers,
                "X-Requested-With": "XMLHttpRequest",
                "anti-csrftoken-a2z": csrf_token,
            },
        )
        await context.add_requests(
            [
                Request.from_url(
                    url=context.request.url,
                    label=f"{self.name}.handler_parse",
                    session_id=context.session.id,
                    always_enqueue=True,
                )
            ]
        )

    async def handler_parse(self, context: ParselCrawlingContext) -> None:
        await self._push_item(context=context)
