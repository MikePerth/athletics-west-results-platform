from pydantic import BaseModel
from app.models.result import Result

class RosterImportRequest(BaseModel):

    competition_id: int
    roster_url: str


