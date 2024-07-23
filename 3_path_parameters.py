from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional, List, Annotated

app = FastAPI()

# Create an in-memory database for demonstration purposes
database = [
    {"name": "John Doe", "email": "john@example.com", "age": 30},
    {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
    {"name": "Alice Brown", "email": "alice@example.com", "age": 28}
]

@app.get("/users/by_name/{user_name}/by_age/{user_age}")
async def get_users_by_name_and_age(
    user_name: Annotated[
        Optional[str],
        Path(
            min_length=2,
            max_length=50,
            regex="^[a-zA-Z0-9 ]*$",
            description="Name of the user to filter by. Must be between 2 and 50 characters long and contain only alphanumeric characters and spaces.",
            title="User Name"
        )
    ],
    user_age: Annotated[
        Optional[int],
        Path(
            ge=0,
            le=120,
            description="Age of the user to filter by. Must be between 0 and 120.",
            title="User Age"
        )
    ]
):
    # Validate parameters
    if user_name is None and user_age is None:
        raise HTTPException(status_code=400, detail="At least one parameter must be provided")
    
    results = database

    if user_name:
        results = [user for user in results if user["name"] and user_name.lower() in user["name"].lower()]

    if user_age is not None:
        results = [user for user in results if user["age"] == user_age]

    if not results:
        raise HTTPException(status_code=404, detail="No users found with the specified criteria")

    return results


    #http://127.0.0.1:8000/users/by_name/john/by_age/30