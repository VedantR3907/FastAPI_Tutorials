import re
import json 
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from fastapi.responses import JSONResponse
from .helper import load_teachers, save_teachers, check_teacher
from .schema import Teacher

router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)

####################################################################################################################################

@router.post("/add-teacher", responses={200: {"description": "Teacher added successfully"}})
async def add_teacher(teacher: Teacher):
    teachers = load_teachers()
    
    # Check if a teacher with the same roll number and class section already exists
    if not check_teacher(teachers, teacher.roll_no):
        raise HTTPException(status_code=400, detail=f"Teacher with roll number {teacher.roll_no} already exists.")
    
    # Add the teacher to the database
    teachers.append(teacher.dict())
    save_teachers(teachers)
    
    return {"message": f"Teacher with ID {teacher.id} has been added successfully"}