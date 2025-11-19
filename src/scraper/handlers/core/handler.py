from typing import TypeVar, Any, cast

from pydantic import BaseModel
from web_poet import (
    HttpResponse,
    ResponseUrl,
    HttpResponseBody,
    WebPage,
    HttpResponseHeaders,
)
from web_poet.utils import ensure_awaitable

from crawlee.crawlers import (
    PlaywrightCrawlingContext,
    ParselCrawlingContext,
    BasicCrawlingContext,
)
from abc import ABC, abstractmethod

from src.utils import walk_module, get_subclasses_from_module
import logging

TItem = TypeVar("TItem")

logger = logging.getLogger(__name__)


class BaseHandler[TContextType: BasicCrawlingContext](ABC):
    name: str  # It MUST match argos response name
    page_class: type[WebPage[Any]]
    proxy: bool = False

    @abstractmethod
    async def _build_poet_response(self, context: TContextType) -> HttpResponse: ...

    async def _context_to_item(
        self,
        context: TContextType,
    ) -> BaseModel:
        page = self.page_class(response=await self._build_poet_response(context))
        try:
            item = await ensure_awaitable(page.to_item())
        except Exception as e:
            logger.exception("Error while converting page to item", exc_info=e)
            raise e
        item = cast(BaseModel, item)
        return item

    async def _push_item(self, context: TContextType) -> None:
        old_item = context.request.user_data.get("item", {})
        old_item = cast(dict[str, Any], old_item)
        if not old_item:
            context.log.warning("Old item not found!")
        new_item = await self._context_to_item(context)
        await context.push_data(old_item | new_item.model_dump())

    async def handler_init(self, context: TContextType) -> None:
        await self._push_item(context)


class PlaywrightHandler(BaseHandler[PlaywrightCrawlingContext], ABC):
    async def _build_poet_response(
        self, context: PlaywrightCrawlingContext
    ) -> HttpResponse:
        html_content = await context.page.content()
        return HttpResponse(
            ResponseUrl(context.page.url),
            body=HttpResponseBody(html_content.encode()),
            headers=HttpResponseHeaders(context.response.headers),
            status=context.response.status,
        )


class HttpHandler(BaseHandler[ParselCrawlingContext], ABC):
    async def _build_poet_response(
        self, context: ParselCrawlingContext
    ) -> HttpResponse:
        return HttpResponse(
            url=ResponseUrl(context.request.url),
            body=HttpResponseBody(await context.http_response.read()),
            headers=HttpResponseHeaders(context.http_response.headers),
            status=context.http_response.status_code,
        )


def discover_handlers(module_name: str) -> dict[str, BaseHandler[Any]]:
    routes_registry: dict[str, BaseHandler[Any]] = {}
    for module in walk_module(module_name):
        if "core" in module.__name__:
            continue
        for subclass in get_subclasses_from_module(module, BaseHandler):
            if subclass.name in routes_registry:
                raise RuntimeError(f"Route {subclass.name} already registered")
            routes_registry[subclass.name] = subclass()
    return routes_registry
