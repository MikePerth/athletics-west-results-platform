# app/schemas/imports.py

from pydantic import BaseModel


class RosterImportDryRunResponse(BaseModel):
    events_found: int
    events_to_create: int

    athletes_found: int
    athletes_existing: int
    athletes_to_create: int

    results_to_create: int
