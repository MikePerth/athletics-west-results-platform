from pydantic import BaseModel
from datetime import date
from typing import Optional


class ResultCreate(BaseModel):
    athlete_id: Optional[int]

    competition_id: int

    event_specification_id: int

    place: Optional[int]

    lane: Optional[int]

    bib: Optional[str]

    performance: Optional[str]

    performance_numeric: Optional[float]

    wind: Optional[float]

    round: Optional[str]

    group_name:[int Optional]

    status: Optional[str]

    competition_date: date