from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header

app = FastAPI()


#####################################################################################
#This is basically using a single async def function into multiple API's
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonsDep, newpara: int):
    commons['newpara'] = newpara
    return commons


@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
#####################################################################################

#Now instead of creating a function we can create a Class

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/classitems/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    return commons

#####################################################################################


#Here we directly raise exception from the dependencies
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/tokenitems/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
