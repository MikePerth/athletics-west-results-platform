from app.models.result import Result
import re

from app.services.performance_utils import (
    normalise_event_name
)

class RosterResultImporter:

    def __init__(
        self,
        session,
        competition
    ):

        self.session = session

        self.competition = competition




   


    def parse_performance_numeric(
        self,
        value
    ):

        if not value:
            return None

        if value in [
            "NM",
            "NH",
            "DQ",
            "DNF",
            "DNS"
        ]:
            return None

        match = re.match(
            r"^([0-9]+(?:\.[0-9]+)?)",
            str(value)
        )

        if match:

            try:

                return float(
                    match.group(1)
                )

            except (
                TypeError,
                ValueError
            ):

                return None

        return None





    def import_events(
        self,
        events
    ):

        imported_count = 0

        for event in events:

            for athlete in event["athletes"]:

                status = athlete.get(
                    "status"
                )

                #
                # Ignore DNS
                #

                if status == "DNS":
                    continue

                result = Result()

                result.competition_id = (
                    self.competition.id
                )

                result.competition_date = (
                    self.competition.start_date
                )

                raw_event_name = event.get(
                    "event_name"
                )

                raw_event_name = event.get(
                    "event_name"
                )

                if raw_event_name:

                    name_upper = raw_event_name.upper()

                    if (
                        "TEAM" in name_upper
                        or "RELAY" in name_upper
                        or "4X" in name_upper
                    ):
                        continue

                result.event_name = (
                    normalise_event_name(
                        raw_event_name
                    )
                )

                result.gender = (
                    event.get("gender")
                )

                result.wind = (
                    athlete.get("wind")
                    if athlete.get("wind") is not None
                    else event.get("wind")
                )

                result.round = event.get(
                    "round"
                )

                result.athlete_name = (
                    athlete.get("name")
                )

                birth_year = athlete.get(
                    "birth_year"
                )

                result.birth_year = (
                    int(birth_year)
                    if birth_year
                    else None
                )

                result.country = (
                    athlete.get("country")
                )

                result.age_group = (
                    athlete.get("age_group")
                )

                result.club = (
                    athlete.get("club")
                )

                place = athlete.get(
                    "place"
                )

                try:

                    result.place = int(place)

                except (
                    TypeError,
                    ValueError
                ):

                    result.place = None

                result.lane = (
                    athlete.get("lane")
                )

                performance = athlete.get(
                    "result"
                )

                if (
                    performance
                    and isinstance(
                        performance,
                        str
                    )
                ):

                    performance = (
                        performance
                        .strip()
                        .rstrip("w")
                    )

                    performance = re.sub(
                        r"\s+[Qq]$",
                        "",
                        performance
                    )

                    performance = re.sub(
                        r"\s+[Qq]$",
                        "",
                        performance
                    )

                    performance = re.sub(
                        r"\s*\((?:NWI|[+-]?\d+(?:\.\d+)?)\)$",
                        "",
                        performance
                    )

                result.performance = (
                    performance
                )

                result.performance_numeric = (
                    self.parse_performance_numeric(
                        performance
                    )
                )

                result.status = status

                result.roster_flag = "Y"

                existing_results = (
                    self.session.query(Result)
                    .filter(
                        Result.competition_id
                        == result.competition_id,

                        Result.athlete_name
                        == result.athlete_name,

                        Result.competition_date
                        == result.competition_date,

                        Result.performance
                        == result.performance,

                        Result.age_group
                        == result.age_group
                    )
                    .all()
                )

                is_duplicate = False

                for existing in existing_results:

                    if (
                        normalise_event_name(
                            existing.event_name
                        )
                        ==
                        normalise_event_name(
                            result.event_name
                        )
                    ):
                        is_duplicate = True
                        break

                if is_duplicate:

                    print(
                        f"SKIPPED DUPLICATE | "
                        f"{result.athlete_name} | "
                        f"{result.event_name} | "
                        f"{result.performance}"
                    )

                    continue


                #print(
                #    f"{result.event_name} | "
                #    f"{result.gender} | "
                #    f"{result.athlete_name}"
                #)

                self.session.add(
                    result
                )

                imported_count += 1

                


        


        self.session.commit()

        return imported_count