from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from schemas import Student, StudentUpdate, StudentResponse, CourseCreate, CourseResponse
from models import StudentModel, CourseModel
from database import get_db
from typing import Optional
from services.students_service import get_student_courses as fetch_student_courses


router = APIRouter(prefix="/students")

@router.post("", response_model=StudentResponse)
def create_students(student: Student, db: Session = Depends(get_db)):
    new_student = StudentModel(
        name=student.name,
        branch=student.branch,
        year=student.year,
        email=student.email
    )
    db.add(new_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    db.refresh(new_student)
    return new_student

@router.post("/{student_id}/courses", response_model=CourseResponse)
def course(student_id:int, course:CourseCreate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    new_course = CourseModel(
        course_name = course.course_name,
        student_id = student_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit:int = Query(default=10, gt=0, le=100),
    branch:Optional[str] = Query(default=None),
    year:Optional[int] = Query(default=None) ,
    sort_by: str = Query(default="name", pattern="^(name|branch|year)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$")
    ):
    query = db.query(StudentModel)
    if branch is not None:
        query = query.filter(StudentModel.branch == branch)
    if year is not None:
        query = query.filter(StudentModel.year == year)
    sort_options = {
        "name": StudentModel.name,
        "branch": StudentModel.branch,
        "year": StudentModel.year
    }

    sort_column = sort_options[sort_by]
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)
    result = query.offset(skip).limit(limit).all()
    return result


@router.get("/{student_id}/courses", response_model=list[CourseResponse])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    return fetch_student_courses(db, student_id)

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    result = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )
    
    student_data = {
        "id": result.id,
        "name": result.name,
        "branch": result.branch,
        "year": result.year,
        "email": result.email
    }
    
    db.delete(result)
    db.commit()
    return {
        "message": "Student deleted successfully",
        "student": student_data
    }

@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    result = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )
    if student_update.name is not None:
        result.name = student_update.name
    if student_update.branch is not None:
        result.branch = student_update.branch
    if student_update.year is not None:
        result.year = student_update.year
    if student_update.email is not None:
        result.email = student_update.email

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    db.refresh(result)
    return result