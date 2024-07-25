import re
from pydantic import BaseModel, Field, validator
from typing import Optional

class Student(BaseModel):
    full_name: Optional[str] = Field(
        default="Name_Not Specified",
        description="This is the Name of the student.",
        pattern=r'^[A-Z][a-zA-Z]*([ ][A-Z][a-zA-Z]*)?$'
    )
    roll_no: Optional[int] = Field(
        default=-1,
        description="This is the unique roll number of each student",
        ge=1,
        le=100
    )
    class_section: Optional[str] = Field(
        default="No_class",
        description="This is the class and the section of the student",
        pattern=r'^[A-Ea-e0-9]+$'
    )
    fees_paid: bool = Field(default=False, description="Has the student paid fees or not")

    @validator('full_name', pre=True, always=True)
    def validate_full_name(cls, v):
        if v and not re.match(r'^[A-Z][a-zA-Z]*([ ][A-Z][a-zA-Z]*)?$', v):
            raise ValueError('Full name must start with a capital letter and only contain letters and a single space.')
        return v
    
class StudentId(Student):
    id: Optional[int] = Field(description="This is a unique ID of each student")  