from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Our fake database
students = [
    {"id": 1, "name": "Ali", "grade": "A"},
    {"id": 2, "name": "Sara", "grade": "B"},
]


# Step 3: Pydantic models
# Used when CREATING a student (POST)
class StudentCreate(BaseModel):
    name: str  # required — must be a string
    grade: Optional[str] = "N/A"  # optional — defaults to "N/A"


# Used when UPDATING a student (PUT)
class StudentUpdate(BaseModel):
    name: Optional[str] = None  # both fields are optional
    grade: Optional[str] = None  # only send what you want to change


# Step 4: GET /students — fetch all
@app.get("/students")
def get_all_students():
    return students  # FastAPI converts to JSON automatically


# Step 5: GET /students/{student_id} — fetch one
@app.get("/students/{student_id}")
def get_one_student(student_id: int):  # type hint in the signature
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


# Step 6: POST /students — create
@app.post("/students", status_code=201)
def add_student(student: StudentCreate):  # Pydantic does all parsing
    new_student = {
        "id": len(students) + 1,
        "name": student.name,  # dot notation — not student['name']
        "grade": student.grade,
    }
    students.append(new_student)
    return new_student


# Step 7: PUT and DELETE
@app.put("/students/{student_id}")
def update_student(student_id: int, update: StudentUpdate):
    for student in students:
        if student["id"] == student_id:
            if update.name is not None:
                student["name"] = update.name
            if update.grade is not None:
                student["grade"] = update.grade
            return student
    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, student in enumerate(students):
        if student["id"] == student_id:
            students.pop(i)
            return {"message": f"Student {student_id} deleted"}
    raise HTTPException(status_code=404, detail="Student not found")


# Step 8: Add the run block and start the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)