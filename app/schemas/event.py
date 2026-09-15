from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Any
import uuid


class EventIngest(BaseModel):
    service_name: str
    event_type: str
    timestamp: datetime
    metadata: dict[str, Any] | None = None

    @field_validator("service_name", "event_type")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be empty")
        return v

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("must be a valid ISO 8601 timestamp e.g. 2024-01-15T10:30:00Z")
        return v


class EventResponse(BaseModel):
    id: uuid.UUID
    service_name: str
    event_type: str
    timestamp: datetime
    metadata: dict[str, Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, event) -> "EventResponse":
        return cls(
            id=event.id,
            service_name=event.service_name,
            event_type=event.event_type,
            timestamp=event.timestamp,
            metadata=event.event_metadata,
            created_at=event.created_at,
        )
