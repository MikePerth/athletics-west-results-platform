from fastapi import (
    APIRouter, 
    Form,
    HTTPException
)

from app.core.database import SessionLocal

from app.models.competition import Competition
from app.models.result import Result

from app.services.roster_competition_importer import (
    RosterCompetitionImporter,
)

from app.services.roster_result_importer import (
    RosterResultImporter,
)

from app.schemas.roster_import import (
    RosterImportRequest,
)

router = APIRouter(
    prefix="/roster",
    tags=["Roster Import"]
)


@router.post("/import")
def import_roster(
    request: RosterImportRequest
):

    session = SessionLocal()

    try:

        competition = session.get(
            Competition,
            request.competition_id
        )

        if not competition:

            raise HTTPException(
                status_code=404,
                detail="Competition not found"
            )

        if not competition.roster_url:

            raise HTTPException(
                status_code=400,
                detail="Competition has no roster URL"
            )

        #
        # Remove previous roster imports
        #

        deleted_count = (
            session.query(Result)
            .filter(
                Result.competition_id == competition.id,
                Result.roster_flag == "Y"
            )
            .delete()
        )

        session.commit()

        #
        # Scrape competition
        #

        scraper = (
            RosterCompetitionImporter(
                competition
            )
        )

        events = (
            scraper.import_competition()
        )

        #
        # Import results
        #

        importer = (
            RosterResultImporter(
                session=session,
                competition=competition
            )
        )

        imported_count = (
            importer.import_events(
                events
            )
        )

        return {
            "success": True,
            "competition_id": competition.id,
            "events_scraped": len(events),
            "results_imported": imported_count,
            "previous_results_deleted": deleted_count
        }

    finally:

        session.close()









@router.post("/roster/import")
def import_roster(

    competition_id: int = Form(...),

    roster_url: str = Form(...)

):

    session = SessionLocal()

    try:

        competition = session.get(
            Competition,
            competition_id
        )

        if not competition:

            raise HTTPException(
                status_code=404,
                detail="Competition not found"
            )

        scraper = RosterCompetitionImporter(
            roster_url
        )

        events = scraper.import_competition()

        importer = RosterResultImporter(
            session=session,
            competition=competition
        )

        imported_count = (
            importer.import_events(
                events
            )
        )

        return {
            "competition_id": competition.id,
            "events_scraped": len(events),
            "results_imported": imported_count
        }

    finally:

        session.close()
