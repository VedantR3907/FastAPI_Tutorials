from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

database = []


# GET REQUESTS
@app.get("/",  summary="This is the my first api", description="This is a discription", response_description="A string")
async def root():
    return {"message": "Hello World"}

@app.get("/user/{email}", description="A get method to get the user detail with email")
async def items(email: str):
    for existing_user in database:
        if existing_user.email == email:
            return {"User_Details": existing_user}
    raise HTTPException(status_code=404, detail="No user found")

#POST REQUEST
class User(BaseModel):
    name: Optional[str] = None
    email: str
    phone: int

@app.post("/users", description="A post method to get the users data")
async def insert_user(user: User):
    for existing_user in database:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    database.append(user)
    
    return JSONResponse(status_code=200, content={"message": "Email inserted into database"})


#UPDATE REQUEST
class Update_User(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None


#depricated means it is old and new one is already out (just for testing)
@app.put("/updateUser/{email}", description="To update users data", deprecated=True)
async def update_user(email: str, user: Update_User):
    for existing_user in database:
        if existing_user.email == email:
            if user.name is not None:
                existing_user.name = user.name
            if user.phone is not None:
                existing_user.phone = user.phone
            
            return JSONResponse(status_code=200, content="User details updated successfully.")
    
    raise HTTPException(status_code=404, detail="No User found")


#DELETE REQUEST
@app.delete("/deleteUser/{email}", description="Deletes user data from database")
async def delete_user(email: str):
    for existing_user in database:
        if existing_user.email == email:
            database.remove(existing_user)
        
            return JSONResponse(content="User deleted successfully", status_code=200)
    
    raise HTTPException(status_code=404, detail = "No User found")