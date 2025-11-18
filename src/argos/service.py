from typing import AsyncIterator
from src.argos.models import ArgosListing, Marketplace
from httpx import Response
import httpx


class AcfService:
    def __init__(self, config: dict[str, str]) -> None:
        self._http_client = httpx.AsyncClient()
        self._token = config["api_token"]
        self._api_url = config["api_url"]

    async def get_listings_without(
        self, field_name: str, routing: int, listing_status: str = "investigating"
    ) -> AsyncIterator[ArgosListing]:
        response = await self._get_from_elastic(
            field_name=field_name,
            routing=routing,
            listing_status=listing_status,
        )
        response.raise_for_status()
        data = response.json()
        hits = data["hits"]["hits"]
        for hit in hits:
            source = hit["_source"]
            yield ArgosListing(
                marketplace=Marketplace(
                    name=source["marketplaceInstance"]["marketplace"]["name"].lower(),
                    region=source["marketplaceInstance"]["country"]["name"],
                ),
                listing_id=hit["_id"],
                url=source["url"],
            )
        iterations = (
            data["hits"]["total"] // 500 + 1
        )  # TODO: Fix potential off-by-one error / What if there are no more hits?
        for offset in range(1, iterations):
            response = await self._get_from_elastic(
                field_name=field_name,
                routing=routing,
                listing_status=listing_status,
                offset=offset * 500,
            )
            response.raise_for_status()
            data = response.json()
            hits = data["hits"]["hits"]
            for hit in hits:
                source = hit["_source"]
                yield ArgosListing(
                    marketplace=Marketplace(
                        name=source["marketplaceInstance"]["marketplace"]["name"],
                        region=source["marketplaceInstance"]["country"]["name"],
                    ),
                    listing_id=hit["_id"],
                    url=source["url"],
                )

    async def _get_from_elastic(
        self,
        field_name: str,
        routing: int,
        listing_status: str,
        offset: int = 0,
        limit: int = 500,
    ) -> Response:
        response = await self._http_client.post(
            f"{self._api_url}/elasticsearch/marketplace/_search",
            params={
                "routing": routing,
            },
            headers={
                "Authorization": self._token,
            },
            json={
                "from": offset,
                "size": limit,
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "term": {
                                    "internalProjectId": routing,
                                },
                            },
                            {
                                "term": {
                                    "moderationStatus": "accepted",
                                },
                            },
                            {
                                "term": {
                                    "internalStatus": listing_status,
                                },
                            },
                            {
                                "bool": {
                                    "should": {
                                        "bool": {
                                            "must_not": {
                                                "exists": {
                                                    "field": field_name,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        ],
                    },
                },
                "sort": [
                    "marketplaceInstance.marketplace.name.keyword",
                    "title.keyword",
                    "_id",
                ],
                "_source": {
                    "includes": [
                        "url",
                        "title",
                        "marketplaceInstance",
                    ],
                },
            },
        )
        return response

    async def batch_update_listings(
        self, listings: list[ArgosListing], routing: int
    ) -> None:
        data = []
        seen = set()
        for listing in listings:
            if listing.username is None or listing.username == "None":
                print(
                    f"Listing ID: {listing.listing_id} does not have a username, skipping."
                )
                continue
            if listing.listing_id in seen:
                print(
                    f"Listing ID: {listing.listing_id} with routing {listing} is a duplicate, skipping."
                )
                continue
            data.append(
                {
                    "id": listing.listing_id,
                    "routing": routing,
                    "body": {"doc": {"seller": {"username": listing.username}}},
                }
            )
            seen.add(listing.listing_id)
        if not data:
            print("No listings to update.")
            return
        response = httpx.put(
            f"{self._api_url}/v1/marketplace/{routing}/items",
            headers={
                "Authorization": self._token,
                "Content-Type": "application/json",
            },
            json=data,
        )
        response.raise_for_status()
        print(f"Batch update response: {response.status_code}, {response.text}")
