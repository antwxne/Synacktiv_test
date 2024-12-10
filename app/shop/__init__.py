from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, Header

from .basket_model import Basket

from .basket_controller import try_insert_basket, OutOfStock

from .product_model import Product
from .checkout_model import Checkout
from .checkout_controller import checkout_controller, BasketIdNotFound
from db_connection import SessionDep
from .stock_controller import add_to_stock, get_all_stock

app: FastAPI = FastAPI()


@app.put("/stock")
async def stock(products: List[Product], session: SessionDep):
    for product in products:
        add_to_stock(product, session)
    session.commit()
    return {"result": "ok"}


@app.get("/stock", response_model=list[Product])
async def stock(session: SessionDep):
    return get_all_stock(session)


@app.post("/basket")
async def basket(basket: Basket, session: SessionDep):
    try:
        try_insert_basket(basket, session)
        return {"result": "ok"}
    except OutOfStock:
        return {"result": "oss"}


@app.post("/checkout")
async def checkout(checkout_id: Checkout, session: SessionDep):
    try:
        return checkout_controller(checkout_id.id, session)
    except BasketIdNotFound:
        return HTTPException(status_code=400, detail="Basket Id not Found")
