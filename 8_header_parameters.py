from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI()

#Basically this is use to set header values (like Tokens etc.) When executing a request you will see a curl command in docs
#which will show the data as -d and heading as -H so this headers will be send as headers instead of data parameter.

@app.get("/read_header/")
async def read_header(
    custom_header: Optional[str] = Header(None)
):
    if custom_header is None:
        raise HTTPException(status_code=400, detail="Custom-Header not found")
    return {"custom_header_value": custom_header}

@app.post("/set_header/")
async def set_header(
    custom_header: Optional[str] = Header(None)
):
    if custom_header is None:
        raise HTTPException(status_code=400, detail="Custom-Header not provided")
    return {"message": f"Received header value: {custom_header}"}