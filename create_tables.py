from app.core.database import Base
from app.core.database import engine

from app.models.competition import Competition
from app.models.result import Result
from app.models.import_batch import ImportBatch

Base.metadata.create_all(bind=engine)

print("Tables created.")