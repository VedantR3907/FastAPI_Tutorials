from fastapi import FastAPI
from .routers.Students import student_apis
from .routers.Teachers import teacher_apis

app = FastAPI()

app.include_router(student_apis.router)
app.include_router(teacher_apis.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the School API's!"}