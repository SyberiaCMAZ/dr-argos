from src.scraper.pages.auction import AuctionDetailsPage
from src.scraper.handlers.core import PlaywrightHandler


# TODO: Could be HTTPRoute it doesn't need JS.
class AuctionDetailsRoute(PlaywrightHandler):
    name: str = "auction"
    page_class: type[AuctionDetailsPage] = AuctionDetailsPage
