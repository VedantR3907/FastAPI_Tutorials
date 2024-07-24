from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

############################################################################

#Simple exception
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
############################################################################

# Custom Exception

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/customexception/{name}")
async def read_unicorn(name: str):
    if name == "vedant":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
############################################################################

# Reusing the Fastapi exception handlers

#This below error is raised when you pass invalid value of request body, so see the last api which
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body}
    )



@app.get("/itemss/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


class Item(BaseModel):
    title: str
    size: int


@app.post("/itemsvalidationerror/")
async def create_item(item: Item):
    return item