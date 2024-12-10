from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Header
from .register_model import Register
from .auth_model import Auth
from .auth_controller import auth_controller, UserDoesNotExist
from .register_controller import register_controller

app: FastAPI = FastAPI()


@app.put("/register")
async def register(user: Register):
    register_controller(user)
    return {"result": "ok"}


@app.post("/auth")
async def register(
    x_user: Annotated[Optional[str], Header()],
    password: Auth,
):
    if x_user is None:
        raise HTTPException(
            status_code=400, detail={"error": "please add X-User header"}
        )
    try:
        if not auth_controller(x_user, password.password):
            raise HTTPException(status_code=401, detail={"result": "unauthorized"})
        return {"result": "ok"}
    except UserDoesNotExist as error:
        raise HTTPException(status_code=401, detail={"error": str(error)})
