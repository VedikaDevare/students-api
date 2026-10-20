
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from .env")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user_id: str):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {
        "sub": user_id,
        "exp": expiration_time
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        return user_id

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )