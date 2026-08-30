from fastapi import (
    APIRouter, 
    Depends,
    HTTPException
)
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






@router.get("/{competition_id}/results")
def competition_results(
    competition_id: int,
    db: Session = Depends(get_db)
):

    competition = (
        db.query(Competition)
        .filter(
            Competition.id == competition_id
        )
        .first()
    )

    if not competition:

        raise HTTPException(
            status_code=404,
            detail="Competition not found"
        )

    results = (
        db.query(Result)
        .filter(
            Result.competition_id == competition_id
        )
        .all()
    )

    events = {}

    for result in results:

        event_name = (
            result.event_name
            if result.event_name
            else "Unknown Event"
        )

        if event_name not in events:

            events[event_name] = []

        events[event_name].append(
            {
                "athlete_name":
                    result.athlete_name,

                "club":
                    result.club,

                "performance":
                    result.performance,

                "place":
                    result.place,

                "wind":
                    result.wind
            }
        )

    #
    # Sort athletes within each event
    #
    for event_name in events:

        events[event_name].sort(
            key=lambda athlete: (
                athlete["place"]
                if athlete["place"] is not None
                else 9999
            )
        )

    #
    # Return events alphabetically for V1
    #
    ordered_events = []

    for event_name in sorted(
        events.keys()
    ):

        ordered_events.append(
            {
                "event_name":
                    event_name,

                "results":
                    events[event_name]
            }
        )

    return {

        "competition_id":
            competition.id,

        "competition_name":
            competition.name,

        "competition_date":
            (
                competition.start_date.strftime(
                    "%d/%m/%Y"
                )
                if competition.start_date
                else None
            ),

        "event_count":
            len(ordered_events),

        "result_count":
            len(results),

        "events":
            ordered_events
    }