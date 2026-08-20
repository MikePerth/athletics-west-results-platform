from sqlalchemy import (
    Column,
    Integer,
    String,
    Date
)

from app.core.database import Base


class Competition(Base):

    __tablename__ = "competitions"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    venue = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    competition_type = Column(String)