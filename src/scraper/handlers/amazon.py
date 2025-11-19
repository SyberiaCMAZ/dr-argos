from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext

from src.scraper.pages.amazon import AmazonDetailsPage
from src.scraper.handlers.core import PlaywrightHandler
from urllib.parse import urlparse


class AmazonDetailsRoute(PlaywrightHandler):
    name: str = "amazon"
    page_class: type[AmazonDetailsPage] = AmazonDetailsPage