from fastapi import FastAPI

from app.api.imports import router as imports_router
from app.api.parse import router as parse_router
from app.models.competition import Competition
from app.models.result import Result
from app.api import athletes
from fastapi.middleware.cors import CORSMiddleware
from app.api import competitions



import app.models

app = FastAPI(
    title="Athletics West Results Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(imports_router)
app.include_router(parse_router)
app.include_router(athletes.router)
app.include_router(
    competitions.router,
    prefix="/competitions",
    tags=["Competitions"]
)

@app.get("/")
def root():

    return {
        "message":
        "Athletics West Results Platform API"
    }