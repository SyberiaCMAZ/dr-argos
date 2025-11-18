import json

from src.scraper.pages.core import BaseDetailsPage
from web_poet import field, cached_method
import logging

import uuid

logger = logging.getLogger(__name__)


class MercadolibreDetailsPage(BaseDetailsPage):

    def _json_ld(self) -> dict:
        json_text = self.xpath('//script[@type="application/ld+json" and contains(text(), "Currency")]/text()').get()
        json_data = json.loads(json_text)
        return json_data

    @field()
    def price(self) -> str:
        return self.xpath('//meta[@itemprop="price"]//following-sibling::span[2]/text()').get()

    @field()
    def currency(self) -> str:
        return  self._json_ld()["offers"]["priceCurrency"]

    @field()
    def username(self) -> str:
        return self.xpath('//div[@class="ui-pdp-seller__header"]//span[@class=""]/text()').get()
