from typing import List
from sqlmodel import select, Session

from .product_model import Product


from .basket_model import Basket, BasketRow


class OutOfStock(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


def possible_to_add_product_to_basket(basket_id: int, product: Product, session: Session) -> bool:
    total_in_stock: int = (
        session.exec(select(Product).where(Product.id == product.id)).one().amount
    )
    total_in_other_basket: int = sum(
        map(
            lambda basket: basket.product_amount,
            session.exec(select(BasketRow).where(BasketRow.product_id == product.id).where(BasketRow.basket_id != basket_id)),
        )
    )
    if total_in_stock < total_in_other_basket + product.amount:
        raise OutOfStock(product.id)
    return True


def try_insert_basket(basket: Basket, session: Session):
    if not all(
        map(
            lambda product: possible_to_add_product_to_basket(basket.id, product, session),
            basket.basket,
        )
    ):
        raise OutOfStock
    basket_to_update: List[BasketRow] = session.exec(
            select(BasketRow).where(BasketRow.basket_id == basket.id)
        )
    for row in basket_to_update:
        session.delete(row)
    session.add_all([BasketRow(
                basket_id=basket.id,
                product_id=product.id,
                product_amount=product.amount,
            ) for product in basket.basket])
    session.commit()
