import argparse
import asyncio
from tools.utils import get_acf_service
import json


async def main(
    routing_id: int,
    field_name: str,
    listing_status: str,
) -> None:
    service = get_acf_service()
    listings = []
    async for listing in service.get_listings_without(
        field_name=field_name,
        routing=routing_id,
        listing_status=listing_status,
    ):
        listings.append(listing)
    print(f"Total listings fetched: {len(listings)}")
    with open("listings_response.json", "w") as f:
        json.dump(
            [listing.model_dump() for listing in listings],
            f,
            ensure_ascii=False,
            indent=4,
        )


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("routing_id", type=int, help="Routing ID for fetching listings")
    args.add_argument(
        "field_name", type=str, help="Field name to check for missing values"
    )
    args.add_argument(
        "--listing_status",
        type=str,
        help="Status to check for missing values",
        default="investigating",
    )
    arguments = args.parse_args()
    asyncio.run(
        main(
            routing_id=arguments.routing_id,
            field_name=arguments.field_name,
            listing_status=arguments.listing_status,
        )
    )
