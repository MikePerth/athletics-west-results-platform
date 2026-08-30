from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.core.database import Base


class AuditLog(Base):

    __tablename__ = "audit_log"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    action = Column(
        String
    )

    entity_type = Column(
        String
    )

    entity_id = Column(
        Integer
    )

    details = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )