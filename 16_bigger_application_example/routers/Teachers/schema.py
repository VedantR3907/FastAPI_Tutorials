import re
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date

class Teacher(BaseModel):
    id: int
    name: str = Field(
        default="Name_Not Specified",
        description="Name of the teacher, should start with capital letters and only contain letters and a single space.",
        pattern=r'^[A-Z][a-zA-Z]*([ ][A-Z][a-zA-Z]*)?$'
    )
    assigned_subjects: List[str] = Field(
        default=[],
        description="List of subjects assigned to the teacher, must be one of the specified values.",
        example=["Mathematics", "Science"],
        min_items=1
    )
    roll_no: int = Field(
        default=-1,
        description="Unique roll number of the teacher, between 1 and 100.",
        ge=1,
        le=100
    )
    salary: float = Field(
        default=-1,
        description="Salary of the teacher, must be greater than or equal to 0.",
        ge=0
    )
    joined_at: date = Field(
        default=date.today(),
        description="Date when the teacher joined, must be less than today's date."
    )

    # Validator for assigned_subjects
    @validator('assigned_subjects', pre=True, always=True)
    def validate_assigned_subjects(cls, v):
        allowed_subjects = {
            "Mathematics", "English Language Arts", "Science", "Social Studies/History",
            "Foreign Language", "Physical Education", "Art", "Music",
            "Technology/Computer Science", "Health Education"
        }
        if not all(subject in allowed_subjects for subject in v):
            raise ValueError(f"Assigned subjects must be one of the following: {', '.join(allowed_subjects)}")
        return v

    # Validator for joined_at
    @validator('joined_at')
    def validate_joined_at(cls, v):
        if v >= date.today():
            raise ValueError("Joined date must be before today's date.")
        return v
