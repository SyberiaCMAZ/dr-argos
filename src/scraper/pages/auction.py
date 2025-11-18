from src.scraper.pages.core import BaseDetailsPage
from web_poet import field
import logging


logger = logging.getLogger(__name__)


class AuctionDetailsPage(BaseDetailsPage):
    @field()
    def price(self) -> str:
        return self.xpath('//script[@type="text/javascript"]/text()').re_first(
            'DCPRICE:\s*?"([\d,]*?)"'
        )

    @field()
    def currency(self) -> str:
        return "KRW"

    @field()
    def username(self) -> str:
        return self.xpath(
            '//span[@class="text__seller"]/a[contains(@href, "stores.auction.co")]/text()'
        ).get()
