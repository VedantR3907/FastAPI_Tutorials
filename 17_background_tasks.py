from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI()

#Basically this Background Tasks are the tasks which take more time to complete so instead of getting the user wait we send the response
#And continue our task in the background.

class Task(BaseModel):
    task_id: int
    task_name: str
    description: Optional[str] = None

tasks_db = []


#Normal function which writes message to task_log file.
def write_log(message: str):
    time.sleep(5)  # Simulating a long-running task
    with open("task_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

@app.post("/add_task", response_model=dict)
async def add_task(task: Task, background_task: BackgroundTasks):
    for existing_data in tasks_db:
        if existing_data['task_id'] == task.task_id:
            raise HTTPException(status_code=404, detail="Task with this task ID already exists")
    
    tasks_db.append(task.model_dump())
    background_task.add_task(write_log, f"Task added: {task.task_name} (ID: {task.task_id})")

    return JSONResponse(status_code=200, content = "Task added successfully")

