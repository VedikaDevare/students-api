from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    courses = relationship("CourseModel", back_populates="student")
    
class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student = relationship("StudentModel", back_populates="courses")
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)