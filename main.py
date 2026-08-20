from fastapi import FastAPI

from app.api.imports import router as imports_router
from app.api.parse import router as parse_router
from app.models.competition import Competition
from app.models.result import Result

import app.models

app = FastAPI(
    title="Athletics West Results Platform"
)

app.include_router(imports_router)
app.include_router(parse_router)


@app.get("/")
def root():

    return {
        "message":
        "Athletics West Results Platform API"
    }