

from app.models.result import Result


from pprint import pprint


def import_results(
    competition_id: int,
    parsed_events,
    competition_date=None
):

    print(f"import_results competition_id = {competition_id}")

    # Build athlete -> club lookup from rows that have clubs
    club_lookup = {}

    for event in parsed_events:
        for result in event["results"]:

            club = result.get("club")

            if club:
                club_lookup[result["athlete_name"]] = club

    # Fill missing clubs
    missing_before = 0
    missing_after = 0

    for event in parsed_events:
        for result in event["results"]:

            # TARGETED DEBUGGING

            

            # Club backfill

            if not result.get("club"):

                missing_before += 1

                result["club"] = club_lookup.get(
                    result["athlete_name"]
                )

            if not result.get("club"):

                missing_after += 1

    print(
        f"Missing clubs before backfill: {missing_before}"
    )

    print(
        f"Missing clubs after backfill: {missing_after}"
    )

    created = 0

    results = []

    for event in parsed_events:

        for parsed_result in event["results"]:

            result = Result(
                competition_id=competition_id,

                event_name=event["event"],
                category=event.get("category"),
                division=event.get("division"),

                age_group=parsed_result.get("age_group"),
                birth_year=parsed_result.get("birth_year"),
                country=parsed_result.get("country"),
                roster_flag=parsed_result.get("roster_flag"),

                athlete_name=parsed_result["athlete_name"],
                club=parsed_result.get("club"),

                place=parsed_result["place"],
                lane=parsed_result.get("lane"),

                performance=parsed_result["performance"],
                performance_numeric=None,

                wind=event["wind"],
                status=parsed_result["status"],

                round=event["round"],
                group_name=event["group"],

                competition_date=competition_date
            )

            results.append(result)
            created += 1

    return results, created
