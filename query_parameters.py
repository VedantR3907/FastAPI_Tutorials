from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define a Pydantic model for the user
class User(BaseModel):
    name: Optional[str] = None
    email: str
    age: int

# Create an in-memory database for demonstration purposes
database = [
    {"name": "John Doe", "email": "john@example.com", "age": 30},
    {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
    {"name": "Alice Brown", "email": "alice@example.com", "age": 28}
]

@app.get("/users/")
async def get_users(name: Optional[str] = Query(None), age: Optional[int] = Query(None)):
    results = database

    if name:
        results = [user for user in results if user["name"] and name.lower() in user["name"].lower()]

    if age:
        results = [user for user in results if user["age"] == age]

    if not results:
        raise HTTPException(status_code=404, detail="No users found with the specified criteria")

    return results

#To hit the API use the following code command: - 
''' http://127.0.0.1:8000/users/?age=25
    http://127.0.0.1:8000/users/?name=john
    http://127.0.0.1:8000/users/?age=30&name=john
'''