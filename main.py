
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm

from database import Base, engine, get_db
from models import StudentModel, CourseModel, UserModel
from routes.students import router
from schemas import UserCreate, UserResponse
from auth import get_current_user, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

password_hash = PasswordHash.recommended()


# Register a new user
@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = UserModel(
        email=user.email,
        hashed_password=password_hash.hash(user.password),
        role="student"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login and generate JWT
@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.email == form_data.username
    ).first()

    password_matches = (
        password_hash.verify(
            form_data.password,
            user.hashed_password
        )
        if user else False
    )

    # Temporary debugging: remove these after testing
    print("User found:", user is not None)
    print("Password matches:", password_matches)

    if not user or not password_matches:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Protected endpoint
@app.get(
    "/protected",
    summary="Access the protected endpoint",
    description="Returns the authenticated user's ID.",
    responses={
        401: {"description": "Authentication credentials are missing or invalid"}
    }
)
def protected_route(user_id: str = Depends(get_current_user)):
    return {
        "message": "You have accessed the protected endpoint!",
        "user_id": user_id
    }


# Include student routes
app.include_router(router)
