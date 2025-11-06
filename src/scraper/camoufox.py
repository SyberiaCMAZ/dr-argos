from camoufox import AsyncNewBrowser
from typing_extensions import override

from crawlee.browsers import (
    PlaywrightBrowserController,
    PlaywrightBrowserPlugin,
)


class CamoufoxPlugin(PlaywrightBrowserPlugin):
    """Example browser plugin that uses Camoufox browser,
    but otherwise keeps the functionality of PlaywrightBrowserPlugin.
    """

    @override
    async def new_browser(self) -> PlaywrightBrowserController:
        if not self._playwright:
            raise RuntimeError("Playwright browser plugin is not initialized.")
        kwargs = self._browser_launch_options | {"headless": True}
        return PlaywrightBrowserController(
            browser=await AsyncNewBrowser(self._playwright, **kwargs),
            # Increase, if camoufox can handle it in your use case.
            max_open_pages_per_browser=1,
            # This turns off the crawlee header_generation. Camoufox has its own.
            header_generator=None,
        )
