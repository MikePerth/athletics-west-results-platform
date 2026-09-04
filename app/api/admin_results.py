from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Result
from app.models.competition import Competition
from app.services.performance_utils import (
    parse_performance_numeric
)



router = APIRouter(
    prefix="/admin/results",
    tags=["Admin Results"]
)




class UpdateResultRequest(BaseModel):

    athlete_name: str | None = None

    birth_year: int | None = None

    country: str | None = None

    club: str | None = None

    age_group: str | None = None

    event_name: str | None = None

    round: str | None = None

    performance: str | None = None

    wind: float | None = None

    place: int | None = None

    lane: str | None = None

    status: str | None = None



class CreateResultRequest(BaseModel):

    competition_id: int

    athlete_name: str

    birth_year: int | None = None

    country: str | None = None

    club: str | None = None

    age_group: str | None = None

    event_name: str

    round: str | None = None

    place: int | None = None

    lane: str | None = None

    performance: str | None = None

    wind: float | None = None

    status: str | None = None

    competition_date: date | None = None





@router.get("")
def get_results(
    athlete_name: str | None = Query(None),
    event_name: str | None = Query(None),
    club: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):

    query = db.query(Result)

    if athlete_name:

        query = query.filter(
            Result.athlete_name.ilike(
                f"%{athlete_name}%"
            )
        )

    if event_name:

        query = query.filter(
            Result.event_name.ilike(
                f"%{event_name}%"
            )
        )

    if club:

        query = query.filter(
            Result.club.ilike(
                f"%{club}%"
            )
        )

    if date_from:

        query = query.filter(
            Result.competition_date >= date_from
        )

    if date_to:

        query = query.filter(
            Result.competition_date <= date_to
        )

    total_count = query.count()

    offset = (
        page - 1
    ) * page_size

    results = (
        query
        .order_by(
            Result.competition_date.desc(),
            Result.athlete_name
        )
        .offset(offset)
        .limit(page_size)
        .all()
    )

    competition_lookup = {
        c.id: c.name
        for c in db.query(
            Competition
        ).all()
    }

    return {

        "page": page,

        "page_size": page_size,

        "total_count": total_count,

        "total_pages": (
            (total_count + page_size - 1)
            // page_size
        ),

        "results": [

            {
                "id": r.id,

                "athlete_name": r.athlete_name,

                "competition_name": (
                    competition_lookup.get(
                        r.competition_id
                    )
                ),

                "competition_date": (
                    r.competition_date.strftime(
                        "%d/%m/%Y"
                    )
                    if r.competition_date
                    else None
                ),

                "event_name": r.event_name,

                "round": r.round,

                "performance": r.performance,

                "wind": r.wind,

                "place": r.place,

                "status": r.status,

                "club": r.club,

                "age_group": r.age_group,

                "birth_year": r.birth_year,

                "country": r.country
            }

            for r in results
        ]
    }




@router.get("/{result_id}")
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = (
        db.query(Result)
        .filter(
            Result.id == result_id
        )
        .first()
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    competition = (
        db.query(Competition)
        .filter(
            Competition.id
            == result.competition_id
        )
        .first()
    )

    return {

        "id": result.id,

        "competition_id": (
            result.competition_id
        ),

        "competition_name": (
            competition.name
            if competition
            else None
        ),

        "competition_date": (
            result.competition_date.strftime(
                "%d/%m/%Y"
            )
            if result.competition_date
            else None
        ),

        "event_name": (
            result.event_name
        ),

        "round": (
            result.round
        ),

        "athlete_name": (
            result.athlete_name
        ),

        "birth_year": (
            result.birth_year
        ),

        "country": (
            result.country
        ),

        "club": (
            result.club
        ),

        "age_group": (
            result.age_group
        ),

        "place": (
            result.place
        ),

        "lane": (
            result.lane
        ),

        "performance": (
            result.performance
        ),

        "performance_numeric": (
            result.performance_numeric
        ),

        "wind": (
            result.wind
        ),

        "status": (
            result.status
        ),

        "group_name": (
            result.group_name
        ),

        "category": (
            result.category
        ),

        "division": (
            result.division
        ),

        "roster_flag": (
            result.roster_flag
        )
    }




@router.put("/{result_id}")
def update_result(
    result_id: int,
    request: UpdateResultRequest,
    db: Session = Depends(get_db)
):

    result = (
        db.query(Result)
        .filter(
            Result.id == result_id
        )
        .first()
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    result.athlete_name = (
        request.athlete_name
    )

    result.birth_year = (
        request.birth_year
    )

    result.country = (
        request.country
    )

    result.club = (
        request.club
    )

    result.age_group = (
        request.age_group
    )

    result.event_name = (
        request.event_name
    )

    result.round = (
        request.round
    )

    result.performance = (
        request.performance
    )

    result.performance_numeric = (
        parse_performance_numeric(
            request.performance,
            request.event_name
        )
    )

    result.wind = (
        request.wind
    )

    result.place = (
        request.place
    )

    result.lane = (
        request.lane
    )

    result.status = (
        request.status
    )

    db.commit()

    db.refresh(result)

    return {
        "message": "Result updated",
        "id": result.id
    }




@router.post("")
def create_result(
    request: CreateResultRequest,
    db: Session = Depends(get_db)
):

    result = Result()

    result.competition_id = (
        request.competition_id
    )

    result.competition_date = (
        request.competition_date
    )

    result.athlete_name = (
        request.athlete_name
    )

    result.birth_year = (
        request.birth_year
    )

    result.country = (
        request.country
    )

    result.club = (
        request.club
    )

    result.age_group = (
        request.age_group
    )

    result.event_name = (
        request.event_name
    )

    result.round = (
        request.round
    )

    result.place = (
        request.place
    )

    result.lane = (
        request.lane
    )

    result.performance_numeric = (
        parse_performance_numeric(
            request.performance
        )
    )

    result.performance = (
        request.performance
    )

    result.wind = (
        request.wind
    )

    result.status = (
        request.status
    )

    result.roster_flag = "N"

    db.add(result)

    db.commit()

    db.refresh(result)

    return {
        "message": "Result created",
        "id": result.id
    }




@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = (
        db.query(Result)
        .filter(
            Result.id == result_id
        )
        .first()
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    db.delete(result)

    db.commit()

    return {
        "message": "Result deleted",
        "id": result_id
    }




