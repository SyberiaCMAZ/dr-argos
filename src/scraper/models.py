from pydantic import BaseModel


class Listing(BaseModel):
    username: str | None
    price: str | None
    currency: str | None
