from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey
    
)

from app.core.database import Base

from app.models.competition import Competition


class Result(Base):

    __tablename__ = "results"

    id = Column(
        Integer,
        primary_key=True
    )

    competition_id = Column(
        Integer,
        ForeignKey("competitions.id")
    )

    event_name = Column(String)

    category = Column(String)
    division = Column(String)
    gender = Column(String)
    age_group = Column(String)
    birth_year = Column(Integer)
    country = Column(String)
    roster_flag = Column(String)

    athlete_name = Column(String)

    club = Column(String)

    place = Column(Integer)

    lane = Column(String)

    performance = Column(String)

    performance_numeric = Column(Float)

    wind = Column(Float)

    status = Column(String)

    round = Column(String)

    group_name = Column(String)

    competition_date = Column(Date)


class Athlete(Base):

    __tablename__ = "athletes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    athlete_name = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    gender = Column(String)

    year_of_birth = Column(Integer)

    primary_club = Column(String)