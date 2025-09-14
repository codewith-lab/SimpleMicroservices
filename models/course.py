from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class CourseBase(BaseModel):
    department_code: str = Field(
        ...,
        description="Department Code",
        json_schema_extra={"example": "COMS"},
    )
    course_code: str = Field(
        ...,
        description="4-digit Course Number",
        json_schema_extra={"example": "4153"},
    )
    title: str = Field(
        ...,
        description="Course Title",
        json_schema_extra={"example": "Cloud Computing"},
    )
    instructor: str = Field(
        ...,
        description="Instructor Name",
        json_schema_extra={"example": "Donald Ferguson"},
    )
    days: str = Field(
        ...,
        description="Class Days",
        json_schema_extra={"example": "MW"},
    )
    start_time: str = Field(
        ...,
        description="Class Start Time",
        json_schema_extra={"example": "1:10PM"},
    )
    end_time: str = Field(
        ...,
        description="Class End Time",
        json_schema_extra={"example": "3:45PM"},
    )
    location: str = Field(
        ...,
        description="Class Location",
        json_schema_extra={"example": "501 NORTHWEST CORNER"},
    )
    size: int = Field(
        ...,
        description="Class Size",
        json_schema_extra={"example": 100},
    )
    credit: int = Field(
        ...,
        description="Course Credit",
        json_schema_extra={"example": 3},
    )
    section: Optional[str] = Field(
        None,
        description="Course Section",
        json_schema_extra={"example": "001"},
    )
    enrollment: Optional[int] = Field(
        None,
        description="Current Enrollment",
        json_schema_extra={"example": 75},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
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
        }
    }

class CourseCreate(CourseBase):
    """ID and created_at are generated on the server side"""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "department_code": "COMS",
                    "course_code": "4776",
                    "title": "Neural Networks & Deep Learning",
                    "instructor": "Richard Zemel",
                    "days": "TT",
                    "start_time": "2:40PM",
                    "end_time": "3:55PM",
                    "location": "833 SEELEY W. MUDD BUILDING",
                    "size": 120,
                    "credit": 3,
                    "section": "001",
                    "enrollment": None,
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update; updated_at are generated on the server side"""
    department_code: Optional[str] = Field(
        None,
        description="Department Code",
        json_schema_extra={"example": "COMS"},
    )
    course_code: Optional[str] = Field(
        None,
        description="4-digit Course Number",
        json_schema_extra={"example": "4153"},
    )
    title: Optional[str] = Field(
        None,
        description="Course Title",
        json_schema_extra={"example": "Cloud Computing"},
    )
    instructor: Optional[str] = Field(
        None,
        description="Instructor Name",
        json_schema_extra={"example": "Donald Ferguson"},
    )
    days: Optional[str] = Field(
        None,
        description="Class Days",
        json_schema_extra={"example": "MW"},
    )
    start_time: Optional[str] = Field(
        None,
        description="Class Start Time",
        json_schema_extra={"example": "1:10PM"},
    )
    end_time: Optional[str] = Field(
        None,
        description="Class End Time",
        json_schema_extra={"example": "3:45PM"},
    )
    location: Optional[str] = Field(
        None,
        description="Class Location",
        json_schema_extra={"example": "501 NORTHWEST CORNER"},
    )
    size: Optional[int] = Field(
        None,
        description="Class Size",
        json_schema_extra={"example": 100},
    )
    credit: Optional[int] = Field(
        None,
        description="Course Credit",
        json_schema_extra={"example": 3},
    )
    section: Optional[str] = Field(
        None,
        description="Course Section",
        json_schema_extra={"example": "001"},
    )
    enrollment: Optional[int] = Field(
        None,
        description="Current Enrollment",
        json_schema_extra={"example": 75},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "department_code": "COMS",
                    "course_code": "4776",
                    "title": "Neural Networks & Deep Learning",
                    "instructor": "Richard Zemel",
                    "days": "TT",
                    "start_time": "2:40PM",
                    "end_time": "3:55PM",
                    "location": "833 SEELEY W. MUDD BUILDING",
                    "size": 120,
                    "credit": 3,
                    "section": "001",
                    "enrollment": None,
                },
                {
                    "days": "MW",
                },
            ]
        }
    }


class CourseRead(CourseBase):
    id: UUID = Field(
        ...,
        description="Persistent Address ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
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
                    "id": "11111111-1111-4111-8111-111111111111",
                    "department_code": "COMS",
                    "course_code": "4776",
                    "title": "Neural Networks & Deep Learning",
                    "instructor": "Richard Zemel",
                    "days": "TT",
                    "start_time": "2:40PM",
                    "end_time": "3:55PM",
                    "location": "833 SEELEY W. MUDD BUILDING",
                    "size": 120,
                    "credit": 3,
                    "section": "001",
                    "enrollment": None,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
