import sqlalchemy.exc
from typing import List
from sqlmodel import select, Session

from .product_model import Product
from .basket_model import BasketRow

class BasketIdNotFound(RuntimeError):
    pass

def checkout_controller(basket_id: int, session: Session) -> List[Product]:
    try:
        basket_content: List[BasketRow] = session.exec(select(BasketRow).where(BasketRow.basket_id == basket_id))
        
        product_list: List[Product] = []
        for basket_row in basket_content:
            product_to_update = session.exec(select(Product).where(Product.id == basket_row.product_id)).one()
            product_to_update.amount -= basket_row.product_amount
            product_list.append(Product(id=basket_row.product_id, amount=basket_row.product_amount))
            session.add(product_to_update)
            session.delete(basket_row)
        session.commit()
        return product_list
    except sqlalchemy.exc.NoResultFound:
        raise BasketIdNotFound