from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
import os

DB_URL: str = os.getenv("DB_URL", "localhost")
DB_USER: str = os.getenv("POSTGRES_USER")
DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
DB_NAME:str = os.getenv("POSTGRES_DB")
connection_url: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}'
engine = create_engine(connection_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]