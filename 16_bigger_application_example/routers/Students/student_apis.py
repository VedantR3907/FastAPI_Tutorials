from fastapi import APIRouter, HTTPException
from typing import Optional, List
from fastapi.responses import JSONResponse
from .helper import load_students, save_students, generate_id, check_student
from .schema import Student, StudentId


router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)  

###################################################################################################################################

@router.post("/add-student", response_model=Student, responses={200: {"description": "student added successfully"}})
async def add_student(student: Student):
    students_data = load_students()

    if not check_student(students_data, student.roll_no, student.class_section):
        raise HTTPException(status_code=400, detail=f"Student already exist with roll number {student.roll_no} in class {student.class_section}")

    student_id = generate_id(students_data)

    student = StudentId(id=student_id, **student.model_dump())
    students_data.append(student.model_dump())
    save_students(students_data)

    return JSONResponse(
        status_code=200,
        content={"message": f"{student.full_name} has been added successfully"}
    )
###################################################################################################################################

@router.put("/edit-student/{student_id}", response_model=Student, responses={200: {"description": "student data updated successfully"}})
async def update_student_data(student_id: int, student: Student):
    students_data = load_students()

    for i in students_data:
        if i['id'] == student_id:

            i.update(student.model_dump(exclude_unset=True))
            save_students(students_data)

            return JSONResponse(
                status_code=200,
                content={"message": f"Student ID {student_id} has been updated successfully"}
            )
    raise HTTPException(status_code=404, detail="Student not found")

###################################################################################################################################

@router.get("/student_data", response_model=List[dict], responses={200: {"description": "Student data fetched successfully"}})
async def filter_students(
    full_name: Optional[str] = None,
    roll_no: Optional[int] = None,
    class_section: Optional[str] = None,
    fees_paid: Optional[bool] = None
):
    students = load_students()

    # Filter students based on provided criteria
    filtered_students = [student for student in students
                         if (full_name is None or student.get('full_name') == full_name)
                         and (roll_no is None or student.get('roll_no') == roll_no)
                         and (class_section is None or student.get('class_section') == class_section)
                         and (fees_paid is None or student.get('fees_paid') == fees_paid)]
    
    return filtered_students

###################################################################################################################################

@router.delete("/delete-student/{student_id}", response_model=dict, responses={200: {"description": "Student deleted successfully"}})
async def delete_student(student_id: int):
    students = load_students()
    
    # Find and remove the student with the given ID
    for student in students:
        if student.get('id') == student_id:
            students.remove(student)
            save_students(students)
            return {"message": f"Student with ID {student_id} has been deleted successfully"}
    
    # If student not found
    raise HTTPException(status_code=404, detail="Student not found")
