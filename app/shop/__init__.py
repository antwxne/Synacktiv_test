from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, Header

from .basket_model import Basket

from .basket_controller import try_insert_basket, OutOfStock

from .product_model import Product
from db_connection import SessionDep
from .stock_controller import add_to_stock, get_all_stock
app: FastAPI = FastAPI()


@app.put("/stock")
async def stock(products: List[Product],session: SessionDep):
    for product in products:
        add_to_stock(product, session)
    session.commit()
    return {"result": "ok"}

@app.get("/stock",  response_model=list[Product])
async def stock(session: SessionDep):
    return get_all_stock(session)

@app.post("/basket")
async def basket(basket: Basket, session: SessionDep):
    try:
        try_insert_basket(basket, session)
        return {"result": "ok"}
    except OutOfStock:
        return {"result": "oss"}