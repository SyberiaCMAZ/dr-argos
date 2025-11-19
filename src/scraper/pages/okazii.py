import json

from src.scraper.pages.core import BaseDetailsPage
from web_poet import field, cached_method
import logging


logger = logging.getLogger(__name__)


class OkaziiDetailsPage(BaseDetailsPage):
    @cached_method
    def _json_ld(self) -> dict:
        json_text = self.xpath('//script[@type="application/ld+json"]/text()').get()
        json_data = json.loads(json_text)["@graph"][0]
        return json_data

    @field()
    def price(self) -> str:
        return str(self._json_ld()["offers"]["price"])

    @field()
    def currency(self) -> str:
        return self._json_ld()["offers"]["priceCurrency"]

    @field()
    def username(self) -> str:
        return self._json_ld()["offers"]["seller"]["name"]
