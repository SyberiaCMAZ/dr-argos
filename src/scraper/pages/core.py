from abc import abstractmethod, ABC

from web_poet import WebPage

from src.scraper.models import Listing


class RequiredFieldMissing(Exception):
    pass


class BaseDetailsPage(WebPage[Listing], ABC):
    @abstractmethod
    def price(self) -> str: ...

    @abstractmethod
    def currency(self) -> str: ...

    @abstractmethod
    def username(self) -> str: ...
