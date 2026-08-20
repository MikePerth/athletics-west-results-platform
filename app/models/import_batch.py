from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.core.database import Base


class ImportBatch(Base):

    __tablename__ = "import_batches"

    id = Column(
        Integer,
        primary_key=True
    )

    filename = Column(String)

    source_type = Column(String)

    status = Column(String)

    uploaded_at = Column(DateTime)

    total_results = Column(Integer)

    total_events = Column(Integer)