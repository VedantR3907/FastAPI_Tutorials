from fastapi import FastAPI
from .routers.Students import students

app = FastAPI()

app.include_router(students.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the School API's!"}