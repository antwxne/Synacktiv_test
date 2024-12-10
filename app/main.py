from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, HTTPException
from calculatrice_controller import calculatrice_controller, InvalidExpression
from totp import app as totp_app
from totp.gpg_utils import SECRETS_FOLDER


app = FastAPI()


@app.on_event("startup")
def on_startup():
    if not os.path.exists(SECRETS_FOLDER):
        os.makedirs(SECRETS_FOLDER)


app.mount("/totp", totp_app)

@app.get("/calculatrice")
def calculatrice(expr: str):
    try:
        return calculatrice_controller(expr)
    except InvalidExpression:
        raise HTTPException(status_code=401, detail=f"Invalid expression: {expr}")
    except ZeroDivisionError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "World"}
