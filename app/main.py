from dotenv import load_dotenv

from db_connection import create_db_and_tables

load_dotenv()
import os
from fastapi import FastAPI, HTTPException
from calculatrice_controller import calculatrice_controller, InvalidExpression
from totp import app as totp_app
from totp.gpg_utils import SECRETS_FOLDER
from shop import app as shop_app


app = FastAPI()


@app.on_event("startup")
def on_startup():
    if not os.path.exists(SECRETS_FOLDER):
        os.makedirs(SECRETS_FOLDER)
    create_db_and_tables()



app.mount("/totp", totp_app)
app.mount("/shop", shop_app)


@app.get("/calculatrice")
def calculatrice(expr: str):
    try:
        return calculatrice_controller(expr)
    except InvalidExpression:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {expr}")
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def read_root():
    return {"Hello": "World"}

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)