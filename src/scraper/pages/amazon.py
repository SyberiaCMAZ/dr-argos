import json

from src.scraper.pages.core import BaseDetailsPage
from web_poet import field
import logging

import uuid

logger = logging.getLogger(__name__)


class AmazonDetailsPage(BaseDetailsPage):
    @field()
    def price(self) -> str:
        return self.xpath(
            '//div[@data-csa-c-content-id="corePrice"]//span[@class="a-offscreen"]'
        ).get()

    @field()
    def currency(self):
        return self.xpath(
            '//div[@id="nav-flyout-icp"]//span[@class="nav-text" and .//a[@class="icp-flyout-change"]]//span[@dir="ltr"][2]/text()'
        ).get()

    @field()
    def username(self) -> str:
        out_of_stock = self.xpath(
            '//div[@id="outOfStock"]//span[@class="a-color-price a-text-bold"]'
        ).get()
        if out_of_stock:
            return "out-of-stock"
        username = self.xpath(
            '//div[@data-feature-name="merchantInfoFeature"]//a[@id="sellerProfileTriggerId"]/text() '
            '| //div[@data-feature-name="merchantInfoFeature"]//div/span[contains(@class, "a-size-small offer-display-feature-text-message")]/text()'
        ).get()
        if not username:
            username = self.xpath(
                '//div[@id="Ebooks-mobile-printSoldBy"]//text()'
            ).get()
            # FIXME: DEBUG ONLY
            if not username:
                with open(f"{uuid.uuid4()}.html", "w", encoding="utf-8") as f:
                    json.dump(
                        {"url": self.url, "context": self.response.text},
                        f,
                        indent=4,
                        ensure_ascii=False,
                    )
                logger.error(f"Username not found for url {self.url}")
        return username
