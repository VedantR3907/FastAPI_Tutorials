from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the form response
class FormResponseModel(BaseModel):
    username: str
    email: str
    age: int

@app.post("/submit_form/")
async def submit_form(
    username: Annotated[str, Form(..., description="The username of the person")],
    email: Annotated[str, Form(..., description="The email address of the person")],
    age: Annotated[int, Form(..., description="The age of the person")]
):
    # Create a response object using the Pydantic model
    response_data = FormResponseModel(username=username, email=email, age=age).dict()
    
    # Return a JSON response
    return JSONResponse(content=response_data)