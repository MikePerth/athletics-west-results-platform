from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_

from app.core.database import get_db
from app.models.result import Result
from app.models.competition import Competition


from app.services.performance_utils import (
    calculate_personal_bests,
    normalise_event_name
)

router = APIRouter(
    prefix="/athletes",
    tags=["Athletes"]
)


@router.get("/search")
def search_athletes(
    q: str = Query(...),
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Result.athlete_name,
            func.max(Result.club).label("club"),
            func.count(Result.id).label("results")
        )
        .filter(
            Result.athlete_name.ilike(f"%{q}%")
        )
        .group_by(
            Result.athlete_name
        )
        .order_by(
            Result.athlete_name
        )
        .all()
    )

    return [
        {
            "athlete_name": r.athlete_name,
            "club": r.club,
            "results": r.results
        }
        for r in results
    ]


@router.get("/{athlete_name}")
def get_athlete_profile(
    athlete_name: str,
    db: Session = Depends(get_db)
):

    performances = (
        db.query(Result)
        .filter(
            Result.athlete_name == athlete_name,
            or_(
                Result.division.is_(None),
                Result.division.like("Multiple%")
            )
        )
        .order_by(
            desc(Result.competition_date)
        )
        .all()
    )

    
    if not performances:
        return None

    latest = performances[0]
        

    #
    # Competition lookup
    #
    competitions = (
        db.query(Competition)
        .all()
    )

    competition_lookup = {
        c.id: c.name
        for c in competitions
    }

    #
    # Personal Bests / Season Bests
    #
    bests = calculate_personal_bests(
        performances
    )

    pb_results = bests.get(
        "personal_bests",
        {}
    )

    sb_results = bests.get(
        "season_bests",
        {}
    )

    return {

        "athlete_name": athlete_name,

        "club": latest.club,

        "country": latest.country,

        "birth_year": latest.birth_year,

        "competition_count": len(
            {
                r.competition_id
                for r in performances
            }
        ),

        "performance_count": len(
            performances
        ),

        "classification_count": 0,

        "personal_bests": [
            {
                "event_name": pb.event_name,

                "performance": pb.performance,

                "wind": pb.wind,

                "is_legal": (
                    pb.wind is None
                    or pb.wind <=2.0
                ),

                "date": (
                    pb.competition_date.strftime(
                        "%d/%m/%Y"
                    )
                    if pb.competition_date
                    else None
                )
            }
            for pb in pb_results.values()
        ],

        "season_bests": [
            {
                "event_name": sb.event_name,

                "performance": sb.performance,

                "wind": sb.wind,

                "is_legal": (
                    sb.wind is None
                    or sb.wind <=2.0
                ),

                "date": (
                    sb.competition_date.strftime(
                        "%d/%m/%Y"
                    )
                    if sb.competition_date
                    else None
                )
            }
            for sb in sb_results.values()
        ],

        "performances": [

            {
                "competition_id": r.competition_id,

                "competition_name": (
                    competition_lookup.get(
                        r.competition_id
                    )
                ),

                "event_name": r.event_name,

                "category": r.category,

                "division": r.division,

                "age_group": r.age_group,

                "round": r.round,

                "performance": r.performance,

                "wind": r.wind,

                "is_legal": (
                    r.wind is None
                    or r.wind <=2.0
                ),

                "place": r.place,

                "competition_date": (
                    r.competition_date.strftime(
                        "%d/%m/%Y"
                    )
                    if r.competition_date
                    else None
                ),
            }

            for r in performances
        ],

        
    }