# app/services/roster_import_preview.py

def build_import_summary(parsed_events):

    athlete_keys = set()
    results_to_create = 0

    for event in parsed_events:

        for result in event["results"]:

            results_to_create += 1

            athlete_keys.add(
                (
                    result["athlete_name"],
                    result["birth_year"],
                )
            )

    return {
        "events_found": len(parsed_events),
        "events_to_create": len(parsed_events),
        "athletes_found": len(athlete_keys),
        "results_to_create": results_to_create,
        "sample_athletes": sorted(
            list(athlete_keys)
        )[:10]
    }