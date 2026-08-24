from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.competition import Competition
from app.models.result import Result

router = APIRouter()





@router.get("/")
def list_competitions(
    db: Session = Depends(get_db)
):

    competitions = (
        db.query(
            Competition.id,
            Competition.name,
            Competition.start_date,
            func.count(Result.id).label(
                "result_count"
            )
        )
        .outerjoin(
            Result,
            Competition.id == Result.competition_id
        )
        .group_by(
            Competition.id
        )
        .order_by(
            Competition.start_date.desc()
        )
        .all()
    )

    return [
        {
            "id": c.id,
            "name": c.name,
            "start_date": (
                c.start_date.strftime("%d/%m/%Y")
                if c.start_date
                else None
            ),
            "result_count": c.result_count
        }
        for c in competitions
    ]