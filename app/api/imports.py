from pathlib import Path

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi import Form
from fastapi import Depends

from app.core.database import get_db

from app.services.performance_utils import (
    parse_performance_numeric
)

from app.services.roster_import_preview import (
    build_import_summary
)

from app.models.competition import Competition
from app.models.result import Result

from app.services.roster_importer import (
    import_results
)

from app.services.roster_parser import (
    extract_text,
    parse_roster_results,
    EVENT_PATTERN
)

router = APIRouter(
    prefix="/imports",
    tags=["Imports"]
)

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/roster")
async def upload_roster_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    raw_text = extract_text(
        str(file_path)
    )

    return {
        "filename": file.filename,
        "characters_extracted": len(raw_text),
        "preview": raw_text[:5000]
    }


@router.post("/roster/import")
async def import_roster_pdf(
    competition_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    raw_text = extract_text(
        str(file_path)
    )

    parsed_events = parse_roster_results(
        raw_text
    )

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
    print(
        f"Competition ID: {competition.id}"
    )

    print(
        f"Competition Start Date: {competition.start_date}"
    )

    results, created, warnings = import_results(
        competition_id,
        parsed_events,
        competition.start_date
    )

    print(
        f"IMPORT_RESULTS RETURNED: "
        f"{len(results)} results"
    )
    existing_count = (
        db.query(Result)
        .filter(
            Result.competition_id == competition_id
        )
        .count()
    )

    if existing_count > 0:

        raise HTTPException(
            status_code=400,
            detail=
                f"Competition already contains "
                f"{existing_count} results. "
                f"Delete existing results before re-importing."
        )
    db.add_all(results)

    print(
        f"ADDING {len(results)} RESULTS"
    )

    db.commit()

    saved_count = (
        db.query(Result)
        .filter(
            Result.competition_id == competition_id
        )
        .count()
    )

    print(
        f"SAVED COUNT = {saved_count}"
    )


@router.post("/roster/preview")
async def preview_roster_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    raw_text = extract_text(
        str(file_path)
    )

    parsed_data = parse_roster_results(
        raw_text
    )

    return {
        "events_found": len(parsed_data),
        "events": parsed_data
    }



@router.post("/roster/dry-run")
async def dry_run_roster_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    raw_text = extract_text(
        str(file_path)
    )

    parsed_data = parse_roster_results(
        raw_text
    )

    return build_import_summary(
        parsed_data
    )




@router.get("/debug/latest")
async def latest_pdf_text():

    files = list(UPLOAD_DIR.glob("*.pdf"))

    if not files:
        return {
            "message": "No PDF files found"
        }

    latest_file = files[0]

    raw_text = extract_text(str(latest_file))

    return {
        "preview": raw_text[:20000]
    }


@router.get("/debug/800m")
async def debug_800m():

    files = list(UPLOAD_DIR.glob("*.pdf"))

    if not files:
        return {"message": "No PDF found"}

    raw_text = extract_text(str(files[0]))

    lines = raw_text.splitlines()

    start = None

    for i, line in enumerate(lines):

        if "800m · Men & Boys · Multiple · Final · Group A" in line:
            start = i
            break

    if start is None:
        return {"message": "800m not found"}

    return {
        "lines": lines[start:start + 30]
    }


@router.get("/debug/events")
async def debug_events():

    files = list(UPLOAD_DIR.glob("*.pdf"))

    raw_text = extract_text(str(files[0]))

    lines = raw_text.splitlines()

    matches = []

    for line in lines:

        if EVENT_PATTERN.search(line):
            matches.append(line)

    return {
        "event_headers": matches
    }


@router.get("/debug/event/{event_name}")
async def debug_event(event_name: str):

    files = list(UPLOAD_DIR.glob("*.pdf"))

    raw_text = extract_text(str(files[0]))

    events = parse_roster_results(raw_text)

    matches = [
        event
        for event in events
        if event_name.lower()
        in event["event"].lower()
    ]

    return {
        "count": len(matches),
        "events": matches
    }