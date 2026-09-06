from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.alert_service import (
    scan_invalid_athlete_names,
    scan_invalid_performances,
    scan_duplicate_athlete_names,
    scan_duplicate_birth_years
)
from datetime import datetime
from fastapi import HTTPException
from app.models.alert import Alert

from pydantic import BaseModel


class ReviewAlertRequest(
    BaseModel
):
    notes: str | None = None



router = APIRouter(
    prefix="/alerts",
    tags=["Admin Alerts"]
)






@router.post(
    "/scan/duplicate-athletes"
)
def scan_duplicate_athletes(
    db: Session = Depends(get_db)
):

    created = (
        scan_duplicate_athlete_names(db)
    )

    return {
        "alerts_created": created
    }







@router.post("/scan")
def scan_all_alerts(
    db: Session = Depends(get_db)
):

    invalid_names = (
        scan_invalid_athlete_names(db)
    )

    invalid_performances = (
        scan_invalid_performances(db)
    )

    duplicate_athletes = (
        scan_duplicate_athlete_names(db)
    )

    duplicate_birth_years = (
        scan_duplicate_birth_years(db)
    )

    return {
        "invalid_names": invalid_names,
        "invalid_performances": invalid_performances,
        "duplicate_athletes": duplicate_athletes,
        "duplicate_birth_years": duplicate_birth_years,
        "total": (
            invalid_names
            + invalid_performances
            + duplicate_athletes
            + duplicate_birth_years
        )
    }







@router.get("")
def get_open_alerts(
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .filter(
            Alert.reviewed == False
        )
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )

    return alerts







@router.get("/reviewed")
def get_reviewed_alerts(
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .filter(
            Alert.reviewed == True
        )
        .order_by(
            Alert.reviewed_at.desc()
        )
        .all()
    )

    return alerts







@router.put("/{alert_id}/review")
def review_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )

    if not alert:

        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.reviewed = True

    alert.reviewed_at = datetime.utcnow()

    db.commit()

    db.refresh(alert)

    return {
        "message": "Alert reviewed",
        "alert_id": alert.id
    }







@router.put("/{alert_id}/review")
def review_alert(
    alert_id: int,
    request: ReviewAlertRequest,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )

    if not alert:

        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.reviewed = True

    alert.reviewed_at = datetime.utcnow()

    alert.notes = request.notes

    db.commit()

    db.refresh(alert)

    return alert







@router.put("/{alert_id}/unreview")
def unreview_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )

    if not alert:

        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.reviewed = False

    alert.reviewed_at = None

    db.commit()

    return {
        "message": "Alert reopened"
    }






@router.get("")
def get_open_alerts(
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .filter(
            Alert.reviewed == False
        )
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )

    results = []

    for alert in alerts:

        item = {
            "id": alert.id,
            "type": alert.type,
            "entity_type": alert.entity_type,
            "entity_id": alert.entity_id,
            "message": alert.message,
            "reviewed": alert.reviewed,
            "created_at": alert.created_at
        }

        if alert.entity_type == "RESULT":

            item["edit_url"] = (
                f"/admin/results/{alert.entity_id}"
            )

        elif alert.entity_type == "ATHLETE":

            item["edit_url"] = (
                f"/admin/athletes/{alert.entity_id}"
            )

        results.append(item)

    return results