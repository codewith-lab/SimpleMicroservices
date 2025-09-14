from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.student import StudentCreate, StudentRead, StudentUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
students: Dict[UUID, StudentRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI(
    title="Student/Course API",
    description="Demo FastAPI app using Pydantic v2 models for Student and Course",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Courses endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    new_id = uuid4()
    now = datetime.utcnow()

    if new_id in courses:
        raise HTTPException(status_code=400, detail="Course with this ID already exists")

    courses[new_id] = CourseRead(
        id=new_id,
        created_at=now,
        updated_at=now,
        **course.model_dump()
    )

    return courses[new_id]


@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    department_code: Optional[str] = Query(None, description="Filter by department code"),
    course_code: Optional[str] = Query(None, description="Filter by course id"),
    title: Optional[str] = Query(None, description="Filter by course title"),
    instructor: Optional[str] = Query(None, description="Filter by instructor"),
    days: Optional[str] = Query(None, description="Filter by class days"),
    start_time: Optional[str] = Query(None, description="Filter by start time"),
    end_time: Optional[str] = Query(None, description="Filter by end time"),
):
    results = list(courses.values())

    if department_code is not None:
        results = [c for c in results if c.department_code.lower() == department_code.lower()]
    if course_code is not None:
        results = [c for c in results if c.course_id == course_code]
    if title is not None:
        results = [c for c in results if title.lower() in c.title.lower()]
    if instructor is not None:
        results = [c for c in results if instructor.lower() in c.instructor.lower()]
    if days is not None:
        results = [c for c in results if days.lower() in c.days.lower()]
    if start_time is not None:
        results = [c for c in results if c.start_time.lower() == start_time.lower()]
    if end_time is not None:
        results = [c for c in results if c.end_time.lower() == end_time.lower()]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    now = datetime.utcnow()
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    stored["updated_at"] = now
    courses[course_id] = CourseRead( **stored)
    return courses[course_id]

@app.delete("/courses/{course_id}", response_model=CourseRead)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    course_to_delete = courses[course_id]
    del courses[course_id]
    return course_to_delete

# -----------------------------------------------------------------------------
# Student endpoints
# -----------------------------------------------------------------------------
@app.post("/students", response_model=StudentRead, status_code=201)
def create_student(student: StudentCreate):
    new_id = uuid4()

    if new_id in courses:
        raise HTTPException(status_code=400, detail="Student with this ID already exists")

    now = datetime.utcnow()
    student_read = StudentRead(
        id=new_id,
        created_at=now,
        updated_at=now,
        **student.model_dump())
    student_read[new_id] = student_read
    return student_read

@app.get("/students", response_model=List[StudentRead])
def list_students(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    major: Optional[str] = Query(None, description="Filter by major"),
    grade: Optional[str] = Query(None, description="Filter by grade"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    department_code: Optional[str] = Query(None, description="Filter by department code of at least one course"),
    instructor: Optional[str] = Query(None, description="Filter by instructor of at least one course"),
):
    results = list(students.values())

    if uni is not None:
        results = [s for s in results if s.uni.lower() == uni.lower()]
    if first_name is not None:
        results = [s for s in results if s.first_name.lower() == first_name.lower()]
    if last_name is not None:
        results = [s for s in results if s.last_name.lower() == last_name.lower()]
    if major is not None:
        results = [s for s in results if s.major.lower() == major.lower()]
    if grade is not None:
        results = [s for s in results if s.grade.lower() == grade.lower()]
    if email is not None:
        results = [s for s in results if s.email == email]
    if phone is not None:
        results = [s for s in results if s.phone == phone]
    if birth_date is not None:
        results = [s for s in results if str(s.birth_date) == birth_date]

    # nested address filtering
    if department_code is not None:
        results = [s for s in results if any(course.department_code.lower() == department_code.lower() for course in s.courses)]
    if instructor is not None:
        results = [s for s in results if any(course.instructor.lower() == instructor.lower() for course in p.courses)]

    return results

@app.get("/students/{student_id}", response_model=StudentRead)
def get_person(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_id[student_id]

@app.patch("/students/{student_id}", response_model=StudentRead)
def update_person(student_id: UUID, update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    now = datetime.utcnow()
    stored = students[student_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    stored['updated_at'] = now
    students[student_id] = StudentRead(**stored)
    return students[student_id]

@app.delete("/students/{student_id}", response_model=StudentRead)
def delete_person(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    student_to_delete = students[student_id]
    del students[student_id]
    return student_to_delete

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Student/Course API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
