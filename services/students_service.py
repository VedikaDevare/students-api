
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import StudentModel


def get_student_courses(db: Session, student_id: int):
    result = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return result.courses
