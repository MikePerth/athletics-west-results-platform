from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Athlete
from app.api import athletes

router = APIRouter()


class UpdateAthleteRequest(BaseModel):

    athlete_name: str
    birth_year: int | None = None
    gender: str | None = None


@router.get("/{athlete_name}")
def get_athlete(
    athlete_name: str,
    db: Session = Depends(get_db)
):
    athlete = (
        db.query(Athlete)
        .filter(
            Athlete.athlete_name == athlete_name
        )
        .first()
    )


    if not athlete:

        raise HTTPException(
            status_code=404,
            detail="Athlete not found"
        )

    return {
        "id": athlete.id,
        "athlete_name": athlete.athlete_name,
        "birth_year": athlete.birth_year,
        "gender": athlete.gender
    }


@router.put("/{athlete_name}")
def update_athlete(
    athlete_name: str,
    request: UpdateAthleteRequest,
    db: Session = Depends(get_db)
):
    athlete = (
        db.query(Athlete)
        .filter(
            Athlete.athlete_name == athlete_name
        )
        .first()
    )

    if not athlete:

        raise HTTPException(
            status_code=404,
            detail="Athlete not found"
        )

    athlete.athlete_name = (
        request.athlete_name
    )

    athlete.birth_year = (
        request.birth_year
    )

    athlete.gender = (
        request.gender
    )

    db.commit()

    db.refresh(athlete)

    return {
        "message": "Athlete updated",
        "id": athlete.id
    }