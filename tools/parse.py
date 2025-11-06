import json
from src.argos.models import ArgosListing
from src.argos.service import AcfService

acf_service = AcfService(
    config={
        "api_url": "https://argos.ebrand.com",
        "api_token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NjI4MDE4NDIsImV4cCI6MTc2MjgzNzg0Miwicm9sZXMiOlsiQWRtaW4iLCJST0xFX0FETUlOIl0sInVzZXJuYW1lIjoibWNod2F0a29AZWJyYW5kLmNvbSIsImlkIjoxMjgwLCJsb2dpbk1ldGhvZCI6InBhc3N3b3JkIn0.ii2sCRwVwpNRnCTCx94orbVlKRBS82tj6TdOqMuGU7A_UQisJmnbGfM0GzCq5EEyEvueMuMVf_LWYGGWdSO7oYOu9pUz4UMJE43DvQCcHLhabp7rNnFcE3ZJhJbb4CwK028j47X_2kbaKDEtoOnKeMX5VqlxQrgKFK9jJUc_9t8SfMB9WdFY00otq5huJKCxwwfAjlWGJtpUeba7HhQQN_xtQT_w-F_ccBH4KpY5K5FqcwSae-vtXzBtNnOKn6qQapUTvcsMQqLFN69nFE-2JSVbOX_9zkFvi8m30Sm3_9g_iHxIM3w8hwPlpEnF7zS0hFmiQZ7R6s4mVB7f1C7sQyY6ddRDXerBWcpLg3rywp9u9KncJ3gPQ9vyHy-KwVE12w-4TC3Z_ZPD0V91RuOrt00p6tnpWMrKobg8FOkpKE020t0eYr_2HWBOqKid0BuEDPl17LH_QexkpiKyVQy-eDf-PqLwZBWa1l9jf5QDNfncTlglLK_tgVEqljZdmxI-h6KJ0hd6QYmyZt4ewexsrbWU_RZ75rxmRLT0b5Z5m1xCYwxbrtSSIUzcucoaBhdGmaEfxH6cGfTSSuFz49r0dTZ8xDBlU6z4mZZX_kdH0_yjpLB112i_n-gXjifXzwnKsjfnst46zr6ptSJZu21ka6Z3cUelym-3S3DWKE4c0SU",
    }
)


async def main():
    with open("listings.json") as f:
        listings = json.load(f)

    ok_listings = []
    out_of_stock_listings = []
    miss_listings = []
    for item in listings:
        listing = ArgosListing(**item)
        if listing.username == "out-of-stock":
            out_of_stock_listings.append(listing)
        elif listing.username:
            if "offer-display-feature-text-message" in listing.username:
                listing.username = "Amazon"
            ok_listings.append(listing)
        else:
            miss_listings.append(listing)

    with open("misses.json", "w") as f:
        json.dump([listing.model_dump() for listing in miss_listings], f)

    print(
        f"ok {len(ok_listings)}"
        f" out of stock {len(out_of_stock_listings)}"
        f" miss {len(miss_listings)}"
        f" total {len(listings)}"
    )
    # with open("dupa.json", "r", encoding="utf-8") as f:
    #     usernames = json.load(f)
    # filed_listings = []
    # for listing in miss_listings:
    #     try:
    #         listing.username = usernames[listing.url]
    #         filed_listings.append(listing)
    #     except KeyError:
    #         continue
    import pdb

    pdb.set_trace()
    user_input = input("press y to push back all listings")
    if user_input == "y":
        await acf_service.batch_update_listings(ok_listings, 3692)


import asyncio

asyncio.run(main())
