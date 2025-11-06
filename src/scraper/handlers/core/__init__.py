from src.scraper.handlers.core.handler import (
    PlaywrightHandler,
    HttpHandler,
    discover_handlers,
)
from src.scraper.handlers.core.router import AutoRouter

__all__ = [
    "HttpHandler",
    "PlaywrightHandler",
    "AutoRouter",
    "discover_handlers",
]
