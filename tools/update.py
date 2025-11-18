import asyncio
import argparse
import json
from src.argos.models import ArgosListing
from tools.utils import get_acf_service


async def main(routing: int):
    acf_service = get_acf_service()
    with open("listings.json", "r", encoding="utf-8") as f:
        listings = json.load(f)
    listings = [ArgosListing(**item) for item in listings]
    await acf_service.batch_update_listings(listings, routing)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("routing_id", type=int, help="Routing ID for updating listings")
    arguments = args.parse_args()
    asyncio.run(main(arguments.routing_id))
