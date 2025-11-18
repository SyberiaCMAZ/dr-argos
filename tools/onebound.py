import re

import requests
import asyncio
from src.argos.models import get_listings, ArgosListing
from tools.utils import get_acf_service
from src.scraper.pages.core import Listing
from pathlib import Path
import json
import sys


def add_to_blocked(listing_id: str):
    with open("blocked.txt", "a") as f:
        f.write(f"{listing_id}\n")


def is_blocked(listing_id: str) -> bool:
    try:
        with open("blocked.txt", "r") as f:
            blocked_ids = f.read().splitlines()
            return listing_id in blocked_ids
    except FileNotFoundError:
        return False


async def main():
    data_path = Path(__file__).parent / "response.json"
    listings = list(get_listings(data_path))
    all_listings = []
    for listing in listings:
        if is_blocked(listing.listing_id):
            continue
        print(listing.url)
        try:
            listing_external_id = re.findall(r"\/item\/(\d*)\.html", listing.url)[0]
        except IndexError:
            add_to_blocked(listing.listing_id)
            continue
        response = requests.get(
            f"https://api-gw.onebound.cn/aliexpress/item_get/?key=qq835830290&secret=ob20201101&num_iid={listing_external_id}",
        )
        try:
            json_data = response.json()
            assert not json_data.get("error") == "item-not-found"
        except (json.JSONDecodeError, AssertionError):
            add_to_blocked(listing.listing_id)
            continue
        item = Listing(
            username=json_data.get("item", {}).get("nick"),
            price=None,
            currency="CNY",
        )
        if item.username is None:
            add_to_blocked(listing.listing_id)
            continue
        print(item)
        all_listings.append(listing.model_dump() | item.model_dump())
    with open("listings.json", "w", encoding="utf-8") as f:
        json.dump(all_listings, f, ensure_ascii=False, indent=4)


async def update_listings():
    with open("listings.json", "r", encoding="utf-8") as f:
        listings = json.load(f)
    service = get_acf_service()
    listings = [ArgosListing(**item) for item in listings]
    await service.batch_update_listings(listings, 533)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "up":
        asyncio.run(update_listings())
    else:
        asyncio.run(main())
