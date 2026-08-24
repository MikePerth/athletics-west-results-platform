from app.core.database import SessionLocal

from app.models.competition import Competition

from app.services.roster_competition_importer import (
    RosterCompetitionImporter
)

from app.services.roster_result_importer import (
    RosterResultImporter
)


def import_roster_competition(
    competition_id
):

    session = SessionLocal()

    competition = session.get(
        Competition,
        competition_id
    )

    if not competition:

        raise ValueError(
            f"Competition {competition_id} not found"
        )

    if not competition.roster_url:

        raise ValueError(
            f"Competition {competition_id} has no roster_url"
        )

    scraper = RosterCompetitionImporter(
        competition
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

    print(
        f"Imported {imported_count} results"
    )

    session.close()


if __name__ == "__main__":
    print("Starting roster import")

    import_roster_competition(
        competition_id=30
    )

    print("Roster import finished")
