from app.core.database import SessionLocal
from app.models import Result
from app.services.performance_utils import normalise_event_name

db = SessionLocal()

updated = 0

try:

    results = db.query(Result).all()

    for result in results:

        original = result.event_name

        normalised = normalise_event_name(
            original
        )

        if normalised != original:

            print(
                f"{result.id}: "
                f"{original} -> {normalised}"
            )

            result.event_name = normalised

            updated += 1

    db.commit()

    print()
    print(
        f"COMPLETE: {updated} records updated."
    )

except Exception:

    db.rollback()
    raise

finally:

    db.close()