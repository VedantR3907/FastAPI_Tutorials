import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent.parent / "Database" / "student_database.json"

def load_students():
    if DATABASE_PATH.exists():
        with open(DATABASE_PATH, "r") as file:
            try:
                data = json.load(file)
                if not data:  # Check if the file is empty
                    return []
                return data
            except json.JSONDecodeError:
                # Handle JSON decoding errors (e.g., if the file is corrupted)
                return []
    return []


# Helper function to save students to JSON file
def save_students(students):
    with open(DATABASE_PATH, "w") as file:
        json.dump(students, file, indent=4)

# Helper function to generate the next student ID
def generate_id(students):
    if students:
        return max(student['id'] for student in students) + 1
    return 1

#Check if student already exists
def check_student(students, new_student_roll_no, new_student_class_section):
    for student in students:
        if student['roll_no'] == new_student_roll_no and student['class_section'] == new_student_class_section:
            return False
    return True