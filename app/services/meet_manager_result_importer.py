from app.models.result import Result
from app.models.competition import Competition
from app.services.performance_utils import (
    parse_performance_numeric,
    normalise_event_name
)

from app.services.gender_utils import (
    normalise_gender
)

class MeetManagerResultImporter:

    def __init__(
        self,
        session
    ):
        self.session = session

    def import_events(
        self,
        competition_id,
        events
    ):

        competition = (
            self.session.query(Competition)
            .filter(
                Competition.id == competition_id
            )
            .first()
        )

        if not competition:
            raise ValueError(
                f"Competition {competition_id} not found"
            )

        for event in events:

            for athlete in event["athletes"]:

                result = Result()

                result.competition_id = competition_id
                
                result.competition_date = (
                    competition.start_date
                )

                normalised_event_name = normalise_event_name(
                    event["event_name"]
                )

                result.event_name = (
                    normalised_event_name
                )

                result.gender = event.get(
                    "gender"
                )

                result.performance = (
                    athlete.get("result")
                )

                result.performance_numeric = (
                    parse_performance_numeric(
                        athlete.get("result"),
                        normalised_event_name
                    )
                )

                result.athlete_name = (
                    athlete["name"]
                )

                result.birth_year = (
                    athlete.get(
                        "birth_year"
                    )
                )

                result.club = (
                    athlete.get("club")
                )

                result.country = (
                    athlete.get("country")
                )

                result.place = (
                    athlete.get("place")
                )
                                               
                result.wind = (
                    athlete.get("wind")
                )

                result.group_name = (
                    athlete.get(
                        "group_name"
                    )
                )

                result.roster_flag = (
                    "N"
                )

                

                self.session.add(result)

        self.session.commit()
                    