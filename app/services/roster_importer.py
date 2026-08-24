from app.models.result import Result
from app.services.performance_utils import normalise_event_name
from app.services.performance_utils import (
    parse_performance_numeric
)


def import_results(
    competition_id: int,
    parsed_events,
    competition_date=None
):

    warnings = []

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

            if not result.get("club"):

                missing_before += 1

                result["club"] = club_lookup.get(
                    result["athlete_name"]
                )

            if not result.get("club"):

                missing_after += 1

    created = 0
    results = []

    # Track imported results so we can suppress
    # generic "Multiple" duplicates
    seen_results = {}

    for event in parsed_events:

        for parsed_result in event["results"]:

            normalised_event = normalise_event_name(
                event["event"]
            )

            if parsed_result.get("status"):
                print(
                    f"IMPORT STATUS: "
                    f"{parsed_result['athlete_name']} "
                    f"{parsed_result['status']}"
                )

            if parsed_result.get("status") == "DNS":
                continue

            dedupe_key = (
                parsed_result["athlete_name"],
                normalised_event,
                event.get("category"),
                event["round"],
                parsed_result["performance"],
                parsed_result.get("status")
            )

            result = Result(
                competition_id=competition_id,

                event_name=normalised_event,

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

                performance_numeric=parse_performance_numeric(
                    parsed_result["performance"],
                    event["event"]
                ),

                wind=(
                    parsed_result.get("wind")
                    if parsed_result.get("wind") is not None
                    else event.get("wind")
                ),

                status=parsed_result["status"],

                round=event["round"],
                group_name=event["group"],

                competition_date=competition_date
            )

            
            existing = seen_results.get(dedupe_key)

            if existing:

                
                existing_division = (
                    existing.division or ""
                )

                new_division = (
                    result.division or ""
                )

                # Prefer age-specific division
                # over generic "Multiple"
                if (
                    existing_division == "Multiple"
                    and new_division.startswith(
                        "Multiple,"
                    )
                ):
                    results.remove(existing)
                    results.append(result)
                    seen_results[dedupe_key] = result

                # Existing record is already
                # the more specific version
                elif (
                    existing_division.startswith(
                        "Multiple,"
                    )
                    and new_division == "Multiple"
                ):
                    pass

                # Otherwise keep first record
                else:
                    pass

            else:

                results.append(result)
                seen_results[dedupe_key] = result

            created += 1
            
    
    
    return results, len(results), warnings