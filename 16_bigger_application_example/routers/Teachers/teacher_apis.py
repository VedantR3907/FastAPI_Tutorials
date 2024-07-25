from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from fastapi.responses import JSONResponse
from .helper import load_teachers, save_teachers, check_teacher, generate_id
from .schema import Teacher, TeacherId
from datetime import date

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

    teacher = TeacherId(id=generate_id(teachers),**teacher.model_dump())
    
    # Check if a teacher with the same roll number and class section already exists
    if not check_teacher(teachers, teacher.roll_no):
        raise HTTPException(status_code=400, detail=f"Teacher with roll number {teacher.roll_no} already exists.")
    
    # Add the teacher to the database
    teachers.append(teacher.model_dump())
    save_teachers(teachers)
    
    return {"message": f"Teacher with ID {teacher.id} has been added successfully"}

####################################################################################################################################

@router.put("/edit-teacher/{teacher_id}", response_model=Teacher, responses={200: {"description": "teacher data updated successfully"}})
async def update_teacher_data(teacher_id: int, teacher: Teacher):
    teachers_data = load_teachers()

    for i in teachers_data:
        if i['id'] == teacher_id:

            i.update(teacher.model_dump(exclude_unset=True))
            save_teachers(teachers_data)

            return JSONResponse(
                status_code=200,
                content={"message": f"Teacher ID {teacher_id} has been updated successfully"}
            )
    raise HTTPException(status_code=404, detail="Teacher not found")

####################################################################################################################################


@router.get("/filter-teachers", response_model=List[Teacher])
async def filter_teachers(
    name: Optional[str] = Query(None, description="Filter by teacher's name"),
    assigned_subjects: Optional[List[str]] = Query(None, description="Filter by assigned subjects"),
    roll_no: Optional[int] = Query(None, ge=1, le=100, description="Filter by roll number"),
    salary: Optional[float] = Query(None, ge=-1, description="Filter by salary"),
    joined_before: Optional[date] = Query(None, description="Filter by joining date before a specific date"),
    joined_after: Optional[date] = Query(None, description="Filter by joining date after a specific date"),
):
    teachers = load_teachers()
    filtered_teachers = [teacher for teacher in teachers
                         if (name is None or teacher.get('name') == name)
                         and (assigned_subjects is None or set(assigned_subjects).intersection(set(teacher.get('assigned_subjects', []))))
                         and (roll_no is None or teacher.get('roll_no') == roll_no)
                         and (salary is None or teacher.get('salary') == salary)
                         and (joined_before is None or date.fromisoformat(teacher.get('joined_at')) < joined_before)
                         and (joined_after is None or date.fromisoformat(teacher.get('joined_at')) > joined_after)]

    return filtered_teachers

####################################################################################################################################

@router.delete("/delete-teacher/{teacher_id}", response_description="Teacher deleted from the database")
async def delete_teacher(teacher_id: int):
    teachers = load_teachers()
    teacher_to_delete = next((teacher for teacher in teachers if teacher["id"] == teacher_id), None)
    
    if not teacher_to_delete:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teachers.remove(teacher_to_delete)
    save_teachers(teachers)
    
    return {"message": f"Teacher with ID {teacher_id} has been deleted successfully"}