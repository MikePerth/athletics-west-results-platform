import re

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.alert import Alert
from app.models.result import Athlete, Result
from app.constants.alert_types import AlertType



INVALID_NAME_PATTERN = re.compile(
    r"[!@#$%^&*()+=\[\]{}|\\<>~`]"
)


def scan_invalid_athlete_names(
    db: Session
) -> int:
    """
    Scan athletes for suspicious characters
    and create alerts for any issues found.

    Returns the number of new alerts created.
    """

    created = 0

    athletes = (
        db.query(Athlete)
        .all()
    )

    for athlete in athletes:

        if not athlete.athlete_name:
            continue

        match = INVALID_NAME_PATTERN.search(
            athlete.athlete_name
        )

        if not match:
            continue

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.type ==
                AlertType.INVALID_ATHLETE_NAME,
                Alert.entity_type == "ATHLETE",
                Alert.entity_id == athlete.id,
                Alert.reviewed == False
            )
            .first()
        )

        if existing_alert:
            continue

        alert = Alert(
            type=AlertType.INVALID_ATHLETE_NAME,
            entity_type="ATHLETE",
            entity_id=athlete.id,
            message=(
                f"Suspicious character "
                f"'{match.group()}' found in athlete name: "
                f"{athlete.athlete_name}"
            )
        )

        db.add(alert)

        created += 1

    db.commit()

    return created








VALID_NON_NUMERIC_RESULTS = {
    "DNF",
    "NM",
    "NH",
    "DQ"
}


PERFORMANCE_PATTERN = re.compile(
    r"^[0-9:\.\-]+$"
)


def scan_invalid_performances(
    db: Session
) -> int:
    """
    Scan for obviously bad performance values.

    We deliberately do NOT flag:
    - NM
    - DNF
    - DQ
    - J1.35 style values

    because they are valid athletics-specific data.

    Returns the number of new alerts created.
    """

    created = 0

    SUSPICIOUS_VALUES = {
        "╖",
        "UWA",
        "UWA LAC",
        "OOC",
        "ING",
        "Belmont Athletics Centre"
    }

    results = (
        db.query(Result)
        .all()
    )

    for result in results:

        performance = (
            result.performance.strip()
            if result.performance
            else ""
        )

        alert_message = None

        #
        # Blank values
        #
        if not performance:

            alert_message = (
                "Performance is blank"
            )

        #
        # Notes imported into performance field
        #
        elif performance.startswith(
            "Notes:"
        ):

            alert_message = (
                f"Notes value stored as "
                f"performance: '{performance}'"
            )

        #
        # Known suspicious values
        #
        elif performance in (
            SUSPICIOUS_VALUES
        ):

            alert_message = (
                f"Suspicious performance "
                f"value: '{performance}'"
            )

        #
        # No issue found
        #
        if not alert_message:
            continue

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.type ==
                AlertType.INVALID_PERFORMANCE,

                Alert.entity_type ==
                "RESULT",

                Alert.entity_id ==
                result.id,

                Alert.reviewed == False
            )
            .first()
        )

        if existing_alert:
            continue

        db.add(
            Alert(
                type=
                AlertType.INVALID_PERFORMANCE,

                entity_type=
                "RESULT",

                entity_id=
                result.id,

                message=
                alert_message
            )
        )

        created += 1

    db.commit()

    return created








def scan_duplicate_birth_years(
    db: Session
) -> int:
    """
    Find athletes that exist with
    multiple birth years.

    Returns the number of new alerts created.
    """

    created = 0

    duplicates = (
        db.query(
            Athlete.athlete_name,
            func.count(
                func.distinct(
                    Athlete.birth_year
                )
            ).label(
                "birth_year_count"
            )
        )
        .filter(
            Athlete.birth_year.isnot(None)
        )
        .group_by(
            Athlete.athlete_name
        )
        .having(
            func.count(
                func.distinct(
                    Athlete.birth_year
                )
            ) > 1
        )
        .all()
    )

    for duplicate in duplicates:

        athlete_name = duplicate.athlete_name

        athlete_records = (
            db.query(Athlete)
            .filter(
                Athlete.athlete_name == athlete_name
            )
            .all()
        )

        athlete_ids = [
            athlete.id
            for athlete in athlete_records
        ]

        birth_years = sorted(
            {
                athlete.birth_year
                for athlete in athlete_records
                if athlete.birth_year is not None
            }
        )

        #
        # Create one alert only
        #
        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.type
                == AlertType.MULTIPLE_BIRTH_YEARS,
                Alert.entity_type
                == "ATHLETE",
                Alert.entity_id
                == athlete_ids[0],
                Alert.reviewed == False
            )
            .first()
        )

        if existing_alert:
            continue

        db.add(
            Alert(
                type=
                AlertType.MULTIPLE_BIRTH_YEARS,

                entity_type="ATHLETE",

                entity_id=
                athlete_ids[0],

                message=(
                    f"Athlete '{athlete_name}' "
                    f"appears with multiple "
                    f"birth years: "
                    f"{', '.join(map(str, birth_years))}"
                )
            )
        )

        created += 1

    db.commit()

    return created









def scan_duplicate_athlete_names(
    db: Session
) -> int:

    created = 0

    duplicates = (
        db.query(
            Athlete.athlete_name,
            func.count(Athlete.id)
        )
        .group_by(
            Athlete.athlete_name
        )
        .having(
            func.count(Athlete.id) > 1
        )
        .all()
    )

    for athlete_name, count in duplicates:

        athletes = (
            db.query(Athlete)
            .filter(
                Athlete.athlete_name == athlete_name
            )
            .all()
        )

        athlete_ids = sorted(
            athlete.id
            for athlete in athletes
        )

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.type ==
                AlertType.POSSIBLE_DUPLICATE_ATHLETE,

                Alert.entity_type ==
                "ATHLETE",

                Alert.entity_id ==
                athlete_ids[0],

                Alert.reviewed == False
            )
            .first()
        )

        if existing_alert:
            continue

        db.add(
            Alert(
                type=
                AlertType.POSSIBLE_DUPLICATE_ATHLETE,

                entity_type=
                "ATHLETE",

                entity_id=
                athlete_ids[0],

                message=(
                    f"Duplicate athlete name "
                    f"'{athlete_name}' found "
                    f"({count} records)"
                )
            )
        )

        created += 1

    db.commit()

    return created
