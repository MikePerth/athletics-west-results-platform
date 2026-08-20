from pathlib import Path

from fastapi import APIRouter

from app.services.roster_parser import extract_text

router = APIRouter(
    prefix="/parse",
    tags=["Parser"]
)


@router.get("/health")
def parser_health():
    return {
        "status": "Parser running"
    }


@router.get("/sample")
def sample_text():

    files = list(
        Path("uploads").glob("*.pdf")
    )

    if not files:
        return {
            "message": "No PDFs uploaded"
        }

    text = extract_text(str(files[0]))

    return {
        "preview": text[:20000]
    }