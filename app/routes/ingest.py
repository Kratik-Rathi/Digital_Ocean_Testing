from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventIngest, EventResponse
from app.services.event_service import create_event
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=EventResponse, status_code=201)
def ingest_event(payload: EventIngest, db: Session = Depends(get_db)):
    try:
        event = create_event(db, payload)
        logger.info(
            "Event ingested",
            extra={
                "event_id": str(event.id),
                "service_name": event.service_name,
                "event_type": event.event_type,
            }
        )
        return EventResponse.from_orm_model(event)
    except Exception as e:
        logger.error("Failed to ingest event", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")
