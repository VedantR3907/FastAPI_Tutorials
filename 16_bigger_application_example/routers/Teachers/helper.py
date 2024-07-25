import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent.parent / "Database" / "teachers_database.json"

# Helper function to load teachers from JSON file
def load_teachers():
    if DATABASE_PATH.exists():
        with open(DATABASE_PATH, "r") as file:
            try:
                data = json.load(file)
                if not data:
                    return []
                return data
            except json.JSONDecodeError:
                return []
    return []

# Helper function to save teachers to JSON file
def save_teachers(teachers):
    with open(DATABASE_PATH, "w") as file:
        json.dump(teachers, file, indent=4, default=str)

def generate_id(teachers):
    if teachers:
        return max(teacher['id'] for teacher in teachers) + 1
    return 1

#Check if teacher already exists
def check_teacher(teachers, new_teacher_roll_no):
    for teacher in teachers:
        if teacher['roll_no'] == new_teacher_roll_no :
            return False
    return True