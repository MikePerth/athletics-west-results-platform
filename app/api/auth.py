from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

from passlib.context import CryptContext

import jwt




pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class LoginRequest(
    BaseModel
):

    username: str

    password: str


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


JWT_SECRET = (
    "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
)

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.username
            == request.username
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=401,
            detail="User disabled"
        )

    valid = pwd_context.verify(
        request.password,
        user.password_hash
    )

    if not valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = jwt.encode(
        {
            "username":
                user.username,
            "is_admin":
                user.is_admin
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "access_token": token,
        "username": user.username
    }


