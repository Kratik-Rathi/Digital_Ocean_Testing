from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.event import Event
from app.schemas.event import EventIngest
import uuid


def create_event(db: Session, payload: EventIngest) -> Event:
    event = Event(
        id=uuid.uuid4(),
        service_name=payload.service_name,
        event_type=payload.event_type,
        timestamp=payload.timestamp,
        event_metadata=payload.metadata,  # updated to match renamed attribute
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_events(
    db: Session,
    service_name: str | None = None,
    event_type: str | None = None,
) -> list[Event]:
    query = db.query(Event)

    if service_name:
        query = query.filter(Event.service_name == service_name)
    if event_type:
        query = query.filter(Event.event_type == event_type)

    return query.order_by(Event.created_at.desc()).all()


def get_summary(
    db: Session,
    service_name: str,
) -> list[dict]:
    results = (
        db.query(Event.event_type, func.count(Event.id).label("count"))
        .filter(Event.service_name == service_name)
        .group_by(Event.event_type)
        .all()
    )

    return [{"event_type": row.event_type, "count": row.count} for row in results]
