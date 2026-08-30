from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)


class CreateUserRequest(
    BaseModel
):

    username: str

    password_hash: str

    is_admin: bool = False


class UpdateUserRequest(
    BaseModel
):

    username: str | None = None

    is_active: bool | None = None

    is_admin: bool | None = None

    password_hash: str | None = None



@router.get("")
def get_users(
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(User.username)
        .all()
    )

    return [

        {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": (
                user.created_at.strftime(
                    "%d/%m/%Y %H:%M"
                )
                if user.created_at
                else None
            )
        }

        for user in users
    ]





@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
    )




@router.post("")
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(User)
        .filter(
            User.username
            == request.username
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User()

    user.username = (
        request.username
    )

    user.password_hash = (
        request.password_hash
    )

    user.is_admin = (
        request.is_admin
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "id": user.id,
        "message": "User created"
    }






@router.put("/{user_id}")
def update_user(
    user_id: int,
    request: UpdateUserRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if request.username is not None:

        user.username = (
            request.username
        )

    if request.is_active is not None:

        user.is_active = (
            request.is_active
        )

    if request.is_admin is not None:

        user.is_admin = (
            request.is_admin
        )

    if request.password_hash:

        user.password_hash = (
            request.password_hash
        )

    db.commit()

    return {
        "message": "User updated"
    }





@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted"
    }






