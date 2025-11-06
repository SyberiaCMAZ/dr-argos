from src.argos.models import get_listings
from pathlib import Path

from src.scraper.container import ScrapingContainer
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)


def filter_out_of_stock(listings):
    out_of_stock_path = Path(__file__).parent.parent / "outofstock.json"
    with out_of_stock_path.open("r") as f:
        data = json.load(f)
    seen_ids = set(l["listing_id"] for l in data)
    for listing in listings:
        if listing.listing_id in seen_ids:
            continue
        yield listing


async def main() -> None:
    data_path = Path(__file__).parent.parent / "parsed.txt"
    listings = list(get_listings(data_path))
    # listings = list(filter_out_of_stock(listings))
    print("Total listings: {}".format(len(listings)))
    container = ScrapingContainer()
    service = container.scraping_service()
    listings = await service.hydrate_listings(listings)
    parsed_listings = [listing.model_dump() for listing in listings]
    with open("listings.json", "w", encoding="utf-8") as f:
        json.dump(parsed_listings, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
