from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .course import CourseBase

# Columbia UNI: 2–3 lowercase letters + 1–4 digits (e.g., abc1234)
UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]

class StudentBase(BaseModel):
    uni: UNIType = Field(
        ...,
        description="Columbia University UNI (2–3 lowercase letters + 1–4 digits).",
        json_schema_extra={"example": "abc1234"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ada"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Lovelace"},
    )
    major: str = Field(
        ...,
        description="Major field of study.",
        json_schema_extra={"example": "Computer Science"},
    )
    grade: str = Field(
        ...,
        description="Current academic grade.",
        json_schema_extra={"example": "Senior"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "ada@example.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1815-12-10"},
    )

    # Embed courses (each with persistent ID)
    courses: List[CourseBase] = Field(
        default_factory=list,
        description="Courses registered to this person for the current semester.",
        json_schema_extra={
            "example": [
                {
                    "department_code": "COMS",
                    "course_code": "4153",
                    "title": "Cloud Computing",
                    "instructor": "Donald Ferguson",
                    "days": "F",
                    "start_time": "1:10PM",
                    "end_time": "3:45PM",
                    "location": "501 NORTHWEST CORNER",
                    "size": 100,
                    "credit": 3,
                    "section": "001",
                    "enrollment": 102,
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "abc1234",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "major": "Computer Science",
                    "grade": "Senior",
                    "phone": "+1-212-555-0199",
                    "birth_date": "1815-12-10",
                    "courses": [
                        {
                            "department_code": "COMS",
                            "course_code": "4153",
                            "title": "Cloud Computing",
                            "instructor": "Donald Ferguson",
                            "days": "F",
                            "start_time": "1:10PM",
                            "end_time": "3:45PM",
                            "location": "501 NORTHWEST CORNER",
                            "size": 100,
                            "credit": 3,
                            "section": "001",
                            "enrollment": 102,
                        }
                    ],
                }
            ]
        }
    }


class StudentCreate(StudentBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "abc1234",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "major": "Computer Science",
                    "grade": "Senior",
                    "phone": "+1-212-555-0199",
                    "birth_date": "1815-12-10",
                    "courses": [
                        {
                            "department_code": "COMS",
                            "course_code": "4153",
                            "title": "Cloud Computing",
                            "instructor": "Donald Ferguson",
                            "days": "F",
                            "start_time": "1:10PM",
                            "end_time": "3:45PM",
                            "location": "501 NORTHWEST CORNER",
                            "size": 100,
                            "credit": 3,
                            "section": "001",
                            "enrollment": 102,
                        }
                    ],
                }
            ]
        }
    }


class StudentUpdate(BaseModel):
    """Partial update for a Student; supply only fields to change."""
    uni: Optional[UNIType] = Field(
        None,
        description="Columbia UNI.",
        json_schema_extra={"example": "ab1234"}
    )
    first_name: Optional[str] = Field(
        None,
        description="Given name.",
        json_schema_extra={"example": "Augusta"})
    last_name: Optional[str] = Field(
        None,
        description="Family name.",
        json_schema_extra={"example": "King"})
    major: Optional[str] = Field(
        None,
        description="Major field of study.",
        json_schema_extra={"example": "Computer Science"},
    )
    grade: Optional[str] = Field(
        None,
        description="Current academic grade.",
        json_schema_extra={"example": "Senior"},
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Primary email address.",
        json_schema_extra={"example": "ada@newmail.com"})
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+44 20 7946 0958"})
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1815-12-10"})
    courses: Optional[List[CourseBase]] = Field(
        None,
        description="Replace the entire set of courses with this list.",
        json_schema_extra={
            "example": [
                {
                    "department_code": "COMS",
                    "course_code": "4153",
                    "title": "Cloud Computing",
                    "instructor": "Donald Ferguson",
                    "days": "F",
                    "start_time": "1:10PM",
                    "end_time": "3:45PM",
                    "location": "501 NORTHWEST CORNER",
                    "size": 100,
                    "credit": 3,
                    "section": "001",
                    "enrollment": 102,
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Ada", "last_name": "Byron"},
                {"phone": "+1-415-555-0199"},
                {
                    "courses": [
                        {
                            "department_code": "COMS",
                            "course_code": "4153",
                            "title": "Cloud Computing",
                            "instructor": "Donald Ferguson",
                            "days": "F",
                            "start_time": "1:10PM",
                            "end_time": "3:45PM",
                            "location": "501 NORTHWEST CORNER",
                            "size": 100,
                            "credit": 3,
                            "section": "001",
                            "enrollment": 102,
                        }
                    ]
                },
            ]
        }
    }


class StudentRead(StudentBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        ...,
        description="Server-generated Student ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "uni": "abc1234",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "major": "Computer Science",
                    "grade": "Senior",
                    "phone": "+1-212-555-0199",
                    "birth_date": "1815-12-10",
                    "courses": [
                        {
                            "department_code": "COMS",
                            "course_code": "4153",
                            "title": "Cloud Computing",
                            "instructor": "Donald Ferguson",
                            "days": "F",
                            "start_time": "1:10PM",
                            "end_time": "3:45PM",
                            "location": "501 NORTHWEST CORNER",
                            "size": 100,
                            "credit": 3,
                            "section": "001",
                            "enrollment": 102,
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
