from fastapi import FastAPI
from .user_model import User

app: FastAPI = FastAPI()

@app.put("/register")
async def register(user: User):
    print(user)
    return "OK"