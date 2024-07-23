from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Set, Dict, Annotated
from fastapi.responses import JSONResponse

app = FastAPI()

database = []

class Item(BaseModel):
    item_id: int
    name: str
    price: int
    tags: List[str] = ["ABC", "DEF"] #default value, Can be set to none

@app.post('/add_item')
async def add_item(item: Item):
    for exisiting_item in database:
        if item.item_id == exisiting_item.item_id:
            raise HTTPException(status_code=400, detail="Item already added")

    database.append(item)
    return JSONResponse(status_code=200, content="Item inserted successfully")



#Nested Models
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


class DataModel(BaseModel):
    data: Dict[int, float]

#Dict example
@app.post("/dict_example/")
async def create_index_weights(data: DataModel):
    return {"received_data": data.data}


    #PASS DATA AS FOLLOWING: - 
    '''{
        "data": {
            "1": 10.5,
            "2": 20.75,
            "3": 30.0
        }
    }'''

# Using Field, which is same as Path and Query but for the pydantic fields.
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/updateitems/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results