from typing import Annotated
from pydantic import BaseModel, StringConstraints


class Auth(BaseModel):
    password: str
