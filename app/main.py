from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from db_connection import create_db_and_tables
from calculatrice_controller import calculatrice_controller, InvalidExpression
from totp import app as totp_app

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


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