from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.meet_manager_pdf_import_service import (
    MeetManagerPdfImportService
)

from app.services.meet_manager_result_importer import (
    MeetManagerResultImporter
)

router = APIRouter(
    prefix="/meet-manager",
    tags=["Meet Manager"]
)




@router.post("/pdf/import")
async def import_meet_manager_pdf(
    competition_id: int = Form(...),
    pdf_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not pdf_file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    parser = MeetManagerPdfImportService()

    events = await parser.import_pdf(
        pdf_file
    )
    
    print(f"EVENTS = {len(events)}")

    if not events:
        print("NO EVENTS EXTRACTED")
        return {
            "success": False,
            "message": "No events extracted from PDF"
        }

    for event in events:

        print(
            f"\n{event['event_name']}"
        )

        print(
            f"ATHLETES = "
            f"{len(event['athletes'])}"
        )

        if event["athletes"]:
            print(
                event["athletes"][0]
            )

    for event in events[:50]:
        print(
            event["event_name"],
            event.get("gender")
    )
    #print(
    #    f"FIRST EVENT ATHLETES = "
    #    f"{len(events[0]['athletes'])}"
    #)



    athlete_count = sum(
        len(event["athletes"])
        for event in events
    )

    print(
        f"TOTAL ATHLETES = {athlete_count}"
    )

    for event in events[:5]:

        print(
            f"{event['event_name']} "
            f"ATHLETES={len(event['athletes'])}"
        )


    result_importer = (
        MeetManagerResultImporter(db)
    )

    result_importer.import_events(
        competition_id,
        events
    )

    athlete_count = sum(
        len(event["athletes"])
        for event in events
    )

    return {
        "competition_id": competition_id,
        "events": len(events),
        "athletes": athlete_count,
        "message": "Meet Manager import completed"
    }
