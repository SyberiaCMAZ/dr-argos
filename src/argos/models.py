from pathlib import Path
import json
from typing import Iterable

from pydantic import BaseModel


class Marketplace(BaseModel):
    name: str
    region: str


class ArgosListing(BaseModel):
    listing_id: str
    url: str
    marketplace: Marketplace
    marketplace_id: int = 0  # <= left for future
    username: str | None = None
    price: str | None = None
    currency: str | None = None


def get_listings(
    file_path: Path, marketplace: str | None = None
) -> Iterable[ArgosListing]:
    with file_path.open("r", encoding="utf8") as file:
        data = json.loads(file.read())
    for listing in data["hits"]["hits"]:
        marketplace_name = listing["_source"]["marketplaceInstance"]["marketplace"][
            "name"
        ].lower()  # <--- Quick dirty fix use marketplace_id later
        if marketplace and marketplace_name != marketplace.lower():
            continue
        yield ArgosListing(
            listing_id=listing["_id"],
            url=listing["_source"]["url"],
            marketplace=Marketplace(
                name=marketplace_name,
                region=listing["_source"]["marketplaceInstance"]["country"]["name"],
            ),
        )


def get_listings_from_service(
    file_path: Path, marketplace: str | None = None
) -> Iterable[ArgosListing]:
    with file_path.open("r", encoding="utf8") as file:
        data = json.loads(file.read())
    for item in data:
        listing = ArgosListing(**item)
        if marketplace and listing.marketplace.name.lower() != marketplace.lower():
            continue
        yield listing
