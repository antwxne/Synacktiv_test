from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user:  str = Field(..., index=True,min_length=4,max_length=16)
    secret: str = Field(...,min_length=8, max_length=64)