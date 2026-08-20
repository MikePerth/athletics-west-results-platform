from pathlib import Path

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi import Form
from fastapi import Depends

from app.core.database import get_db

from app.services.roster_import_preview import (
    build_import_summary
)

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

    # TEMPORARY DUPLICATE DIAGNOSTIC

    seen = set()
    duplicates_found = 0

    for event in parsed_events:

        for parsed_result in event["results"]:

            key = (
                event["event"],
                parsed_result.get("athlete_name"),
                parsed_result.get("performance"),
                parsed_result.get("place"),
                parsed_result.get("club"),
                parsed_result.get("status")
            )

            if key in seen:

                duplicates_found += 1

                print(
                    f"DUPLICATE FOUND: {key}"
                )

            else:

                seen.add(key)

    print(
        f"Duplicate result combinations detected: "
        f"{duplicates_found}"
    )

    results, created = import_results(
        competition_id,
        parsed_events
    )

    db.add_all(results)

    db.commit()

    return {
        "competition_id": competition_id,
        "events_imported": len(parsed_events),
        "results_created": created
    }

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