from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventResponse
from app.services.event_service import get_events, get_summary
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/events", response_model=list[EventResponse])
def list_events(
    service_name: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    events = get_events(db, service_name=service_name, event_type=event_type)
    logger.info(
        "Events retrieved",
        extra={
            "count": len(events),
            "service_name": service_name,
            "event_type": event_type,
        }
    )
    return [EventResponse.from_orm_model(e) for e in events]


@router.get("/events/summary")
def events_summary(
    service_name: str = Query(...),
    db: Session = Depends(get_db),
):
    summary = get_summary(db, service_name=service_name)
    logger.info(
        "Summary retrieved",
        extra={"service_name": service_name}
    )
    return {
        "service_name": service_name,
        "summary": summary
    }
