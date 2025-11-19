from src.scraper.pages.amazon import AmazonDetailsPage
from src.scraper.handlers.core import PlaywrightHandler


class AmazonDetailsRoute(PlaywrightHandler):
    name: str = "amazon"
    page_class: type[AmazonDetailsPage] = AmazonDetailsPage
