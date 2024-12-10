from typing import List
from sqlmodel import select, Session
import sqlalchemy.exc


from .product_model import Product
from db_connection import SessionDep



def add_to_stock(product: Product, session: Session):
        statement = select(Product).where(Product.id == product.id)
        try:
            results = session.exec(statement)
            product_to_update = results.one()
            product_to_update.amount += product.amount
            session.add(product_to_update)
        except sqlalchemy.exc.NoResultFound:
            session.add(product)

def get_all_stock(session: Session) -> List[Product]:
    return session.exec(select(Product))