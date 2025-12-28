from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate, StudentStats, PaginatedStudentResponse
from app.services.student_service import StudentService
from app.api.v1.dependencies import get_student_service
from typing import List, Optional

router = APIRouter()


@router.get("/students/all", response_model=List[StudentRead])
async def get_all_students(service: StudentService = Depends(get_student_service)):
    """
    Get all students without pagination (for statistics).
    """
    return await service.list_students()


@router.get("/students", response_model=PaginatedStudentResponse)
async def get_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    grade: Optional[str] = None,
    class_type: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    service: StudentService = Depends(get_student_service)
):
    """
    Get students with pagination, filtering, and sorting.
    """
    return await service.list_students_paginated(
        page=page,
        page_size=page_size,
        search=search,
        grade=grade,
        class_type=class_type,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/students/{student_id}", response_model=StudentRead)
async def get_student(
    student_id: int, service: StudentService = Depends(get_student_service)
):
    """
    Get a specific student by ID.
    """
    student = await service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/students", response_model=StudentRead, status_code=201)
async def create_student(
    student: StudentCreate, service: StudentService = Depends(get_student_service)
):
    """
    Create a new student with scores.
    Grades are automatically calculated.
    """
    return await service.create_student(student)


@router.put("/students/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    """
    Update a student's information and scores.
    Grades are automatically recalculated.
    """
    updated_student = await service.update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


@router.delete("/students/{student_id}", status_code=204)
async def delete_student(
    student_id: int, service: StudentService = Depends(get_student_service)
):
    """
    Delete a student.
    """
    success = await service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return None


@router.get("/students/stats/overview", response_model=StudentStats)
async def get_statistics(
    service: StudentService = Depends(get_student_service)
):
    """
    Get statistics about all students including:
    - Total students
    - Pass/Fail counts
    - Grade distribution
    - Subject-wise pass/fail statistics
    """
    return await service.get_statistics()


@router.get("/students/stats/detailed")
async def get_detailed_statistics(
    class_type: Optional[str] = None,
    service: StudentService = Depends(get_student_service)
):
    """
    Get detailed analytics including:
    - Subject average scores
    - Score distribution by ranges
    - Performance metrics by class type
    - Gender-based statistics
    """
    return await service.get_detailed_statistics(class_type)

