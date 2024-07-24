from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, time, timedelta

app = FastAPI()

# Define a Pydantic model for the request body
class DataModel(BaseModel):
    uuid: UUID
    date: date
    time: time
    duration: timedelta

@app.post("/submit_data/")
async def submit_data(data: DataModel):
    # Example processing (just return the received data for demonstration)
    return {
        "uuid": data.uuid,
        "date": data.date,
        "time": data.time,
        "duration": data.duration
    }