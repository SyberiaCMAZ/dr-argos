from src.scraper.pages.okazii import OkaziiDetailsPage
from src.scraper.handlers.core import HttpHandler


class OkaziiDetailsRoute(HttpHandler):
    name: str = "okazii"
    page_class: type[OkaziiDetailsPage] = OkaziiDetailsPage
