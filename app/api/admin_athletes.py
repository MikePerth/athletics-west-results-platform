from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Athlete, Result
from app.api import athletes

router = APIRouter()


class UpdateAthleteRequest(BaseModel):

    athlete_name: str
    birth_year: int | None = None
    gender: str | None = None




class MergeAthleteRequest(BaseModel):

    source_name: str

    target_name: str




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






@router.post("/merge")
def merge_athletes(
    request: MergeAthleteRequest,
    db: Session = Depends(get_db)
):

    source_name = (
        request.source_name
        .strip()
    )

    target_name = (
        request.target_name
        .strip()
    )

    if not source_name:

        raise HTTPException(
            status_code=400,
            detail="Source athlete is required"
        )

    if not target_name:

        raise HTTPException(
            status_code=400,
            detail="Target athlete is required"
        )

    if (
        source_name.lower()
        ==
        target_name.lower()
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Source and target athletes "
                "cannot be the same"
            )
        )

    source_results = (
        db.query(Result)
        .filter(
            Result.athlete_name
            == source_name
        )
        .all()
    )

    if not source_results:

        raise HTTPException(
            status_code=404,
            detail="Source athlete not found"
        )

    merged_results = len(
        source_results
    )

    for result in source_results:

        result.athlete_name = (
            target_name
        )

    db.commit()

    return {
        "message": (
            "Athletes merged successfully"
        ),
        "merged_results":
            merged_results,
        "source_name":
            source_name,
        "target_name":
            target_name
    }