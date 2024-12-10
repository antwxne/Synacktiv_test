from typing import Annotated
from pydantic import BaseModel, StringConstraints

class Register(BaseModel):
    user:  Annotated[str, StringConstraints(min_length=4,max_length=16)]
    secret: Annotated[str, StringConstraints(min_length=8,max_length=64)]