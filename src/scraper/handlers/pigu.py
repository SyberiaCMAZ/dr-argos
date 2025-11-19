from src.scraper.pages.pigu import PiguDetailsPage
from src.scraper.handlers.core import PlaywrightHandler


class PiguDetailsRoute(PlaywrightHandler):
    name: str = "pigu"
    page_class: type[PiguDetailsPage] = PiguDetailsPage
