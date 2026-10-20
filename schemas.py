from pydantic import BaseModel, Field, EmailStr
class Student(BaseModel):
    name : str = Field(min_length=2, max_length=50)
    branch : str = Field(min_length=2, max_length=20)
    year : int = Field(gt=0, le=4)
    email : EmailStr
    
class StudentUpdate(BaseModel):
    name: str | None = None
    branch: str | None = None
    year: int | None = None
    email: EmailStr | None = None
class StudentResponse(BaseModel):
    id: int
    name: str
    branch: str
    year: int
    email: EmailStr

    class ConfigDict:
        from_attributes = True
class CourseCreate(BaseModel):
    course_name : str = Field(min_length=2, max_length=50)
    student_id : int = Field(gt=0)
class CourseResponse(BaseModel):
    course_name : str
    student_id : int
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}