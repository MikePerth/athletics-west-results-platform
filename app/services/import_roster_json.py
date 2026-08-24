import sys
import json

from app.core.database import SessionLocal
from app.models.competition import Competition

from app.services.roster_result_importer import (
    RosterResultImporter
)

competition_id = int(sys.argv[1])

session = SessionLocal()

competition = (
    session.query(Competition)
    .get(competition_id)
)

with open(
    "roster_events.json",
    encoding="utf-8"
) as f:

    events = json.load(f)

importer = RosterResultImporter(

    session=session,

    competition=competition

)

importer.import_events(
    events
)