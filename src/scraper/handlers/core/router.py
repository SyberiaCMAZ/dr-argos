from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar, Any

from crawlee._types import BasicCrawlingContext  # noqa

from src.scraper.handlers.core.handler import BaseHandler

TCrawlingContext = TypeVar("TCrawlingContext", bound=BasicCrawlingContext)
RequestHandler = Callable[[TCrawlingContext], Awaitable[None]]


class AutoRouter(Generic[TCrawlingContext]):
    """
    Implementation of crawlee.Router that integrates with BaseRoute class.

    This class uses a request.label to select appropriate BaseRoute class.
    """

    def __init__(self, handlers_registry: dict[str, BaseHandler[Any]]) -> None:
        self._handlers_registry = handlers_registry

    async def __call__(self, context: TCrawlingContext) -> None:
        if context.request.label is None:
            raise RuntimeError("No request label")
        handler_name, handler_func = context.request.label.split(".", 1)
        if handler_name not in self._handlers_registry:
            context.request.no_retry = True
            raise RuntimeError(f"No handler matches label `{context.request.label}`")
        handler = getattr(self._handlers_registry[handler_name], handler_func)
        return await handler(context)
