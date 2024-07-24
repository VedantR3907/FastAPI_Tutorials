from fastapi import FastAPI, HTTPException, Cookie
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

# Define a Pydantic model for the request body
class CookieModel(BaseModel):
    value: str

@app.get("/read_cookie/")
async def read_cookie(my_cookie: Optional[str] = Cookie(None)):
    if my_cookie is None:
        return JSONResponse(content={"message": "No cookie found"}, status_code=404)
    return {"cookie_value": my_cookie}

@app.post("/set_cookie/")
async def set_cookie(cookie: CookieModel):
    response = JSONResponse(content={"message": "Cookie set"})
    response.set_cookie(key="my_cookie", value=cookie.value)
    return response

@app.post("/delete_cookie/")
async def delete_cookie(cookie: CookieModel):
    response = JSONResponse(content={"message": "Cookie deleted"})
    response.delete_cookie(key="my_cookie")
    return response