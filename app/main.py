from fastapi import FastAPI, HTTPException
from calculatrice_controller import calculatrice_controller, InvalidExpression
app = FastAPI()

@app.get("/calculatrice")
def calculatrice(expr: str):
    try:
        return calculatrice_controller(expr)
    except InvalidExpression:
        raise HTTPException(status_code=401, detail=f"Invalid expression: {expr}") 


@app.put("/totp/register")
def calculatrice(expr: str):
    try:
        return calculatrice_controller(expr)
    except InvalidExpression:
        raise HTTPException(status_code=401, detail=f"Invalid expression: {expr}") 



@app.get("/")
def read_root():
    return {"Hello": "World"}