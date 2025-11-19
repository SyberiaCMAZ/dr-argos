from src.scraper.pages.core import BaseDetailsPage
from web_poet import field, cached_method
import json


class PiguDetailsPage(BaseDetailsPage):
    @cached_method
    def _json_ld(self) -> dict:
        json_text = self.xpath(
            '//script[@type="application/ld+json" and contains(text(), "Currency")]/text()'
        ).get()
        json_data = json.loads(json_text)
        return json_data

    @field()
    def price(self) -> str:
        return self._json_ld()["offers"]["price"]

    @field()
    def currency(self) -> str:
        return self._json_ld()["offers"]["priceCurrency"]

    @field()
    def username(self) -> str:
        return self.xpath(
            '//a[contains(@gtm-t-l, "product_seller_summary")]/span/text()'
        ).get()
