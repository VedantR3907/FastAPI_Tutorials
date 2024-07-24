from typing import Any
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr

app = FastAPI()

########################################################################################################
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


#Below if you dont return it with list of items then we will get internal server error
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]



########################################################################################################
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


#In the following API we may take input as UserIn but we will get output all the parameters of UserOut
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


########################################################################################################
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


########################################################################################################
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


#The response_model_exclude_unset, excludes the parameters which are not passed from the request body so in the below example
#When you try to get data of foo then we will get data as written below but when you remove the response_model_exclude_unset
#You will get all the above parameters with there default values too. So basically it removes the parameters which are not passed.

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
########################################################################################################