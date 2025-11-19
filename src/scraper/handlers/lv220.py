from src.scraper.pages.pigu import PiguDetailsPage
from src.scraper.handlers.core import HttpHandler


class lv220DetailsRoute(HttpHandler):
    name: str = "220"
    page_class: type[PiguDetailsPage] = PiguDetailsPage
