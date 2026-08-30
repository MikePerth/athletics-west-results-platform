from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Result
from app.models.competition import Competition
from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    athlete_count = (
        db.query(
            Result.athlete_name
        )
        .distinct()
        .count()
    )

    return {

        "competitions": (
            db.query(
                Competition
            ).count()
        ),

        "athletes": athlete_count,

        "results": (
            db.query(
                Result
            ).count()
        ),

        "users": (
            db.query(
                User
            ).count()
        )
    }