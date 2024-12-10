from typing import List
from sqlmodel import Field, SQLModel
from pydantic import BaseModel
from .product_model import Product


class BasketRow(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    basket_id: int = Field(index=True)
    product_id: int = Field(index=True)
    product_amount: int = Field()


class Basket(BaseModel):
    id: int
    basket: List[Product]
