from src.scraper.pages.mercadolibre import MercadolibreDetailsPage
from src.scraper.handlers.core import PlaywrightHandler


class MercadolibreDetailsRoute(PlaywrightHandler):
    name: str = "mercadolibre"
    page_class: type[MercadolibreDetailsPage] = MercadolibreDetailsPage
    proxy: bool = True
