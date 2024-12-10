from pydantic import BaseModel


class Checkout(BaseModel):
    id: int
