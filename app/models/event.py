import uuid
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    event_metadata = Column("metadata", JSON, nullable=True)  # renamed attribute, DB column stays "metadata"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
