import re
from datetime import date

def is_field_event(event_name: str) -> bool:

    field_keywords = [
        "Jump",
        "Vault",
        "Throw",
        "Discus",
        "Shot Put",
        "Javelin",
        "Hammer"
    ]

    return any(
        keyword in event_name
        for keyword in field_keywords
    )


def is_track_event(event_name: str) -> bool:

    return not is_field_event(event_name)

def is_legal_for_records(result):

    if result.wind is None:
        return True

    return result.wind <= 2.0



def is_current_season(competition_date):

    if not competition_date:
        return False

    today = date.today()

    #
    # Athletics season:
    # 1 October -> 30 April
    #

    if today.month >= 10:
        season_start_year = today.year
    else:
        season_start_year = today.year - 1

    season_start = date(
        season_start_year,
        10,
        1
    )

    season_end = date(
        season_start_year + 1,
        4,
        30
    )

    return (
        season_start
        <= competition_date
        <= season_end
    )



def normalise_event_name(event_name: str) -> str:
    
    event_name = event_name.strip()
    
    event_name = re.sub(
        r"^Multiple\s+group\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    #
    # Fix mangled middle-dot character
    #

    event_name = event_name.replace(
        "╖",
        "·"
    )

    #
    # Remove finals / heats
    #

    if "·" in event_name:

        event_name = (
            event_name
            .split("·")[0]
            .strip()
        )
    # U13 - U18 - Site 1 Javelin Throw
    event_name = re.sub(
        r"^U\d+\s*-\s*U\d+\s*-\s*",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # 200m Hurdles (76.2cm / 18.29m)
    # 80m Hurdles (76.2cm / 7m)
    # 400m Hurdles (91.4cm / 35m)
    event_name = re.sub(
        r"\s*\([^)]*cm\s*/\s*[^)]*\)",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # Javelin Throw (400g)
    # Shot Put (3kg)
    # Discus Throw (1kg)
    # Hammer Throw (4kg)
    event_name = re.sub(
        r"\s*\((?:[\d.]+(?:kg|g))\)",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # U13 - U18 Javelin Throw
    event_name = re.sub(
        r"^U\d+\s*-\s*U\d+\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # U13 - 18 Javelin Throw
    event_name = re.sub(
        r"^U\d+\s*-\s*\d+\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # Remove leading dash
    event_name = re.sub(
        r"^\s*-\s*",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    event_name = re.sub(
        r"\s*\([^)]*cm\s*/\s*[^)]*\)",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # Site 1. High Jump
    event_name = re.sub(
        r"^Site\s*\d+\.?\s*",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # Remove hurdle specifications
    # (76.2cm / 18.29m)
    # (91.4cm / 35m)

    event_name = re.sub(
        r"\s*\([^)]*cm\s*/\s*[^)]*\)",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # Remove implement weights
    # (400g)
    # (3kg)
    # (1kg)

    event_name = re.sub(
        r"\s*\((?:[\d.]+(?:kg|g))\)",
        "",
        event_name,
        flags=re.IGNORECASE,
    )


    # Site - 1 (FA)/ 3 (FB) Triple Jump
    event_name = re.sub(
        r"^Site\s*-\s*\d+\s*\(FA\)\s*/\s*\d+\s*\(FB\)\s*",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # 76cm 80m Hurdles
    # 76.2cm 200m Hurdles
    # 0.762m 80m Hurdles
    event_name = re.sub(
        r"^\d+(?:\.\d+)?cm\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    # U20 - Open Hammer Throw
    # U20 and Open Hammer Throw
    # U20 to Open Discus Throw

    event_name = re.sub(
        r"^U20\s*(?:-|and|to)\s*Open\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # Remove site/pit prefixes
    event_name = re.sub(
        r"^\(Pit\s*\d+\)\s*",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    event_name = re.sub(
        r"^Site\s*\d+\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )

    event_name = re.sub(
        r"^Mcgillivray\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
    # U20-Open Triple Jump

    event_name = re.sub(
        r"^U20-Open\s+",
        "",
        event_name,
        flags=re.IGNORECASE,
    )
# LA Hurdles 68cm 80m Hurdles
# LA Hurdles 68cm 200m Hurdles

    event_name = re.sub(
        r"^LA\s+Hurdles\s+\d+(?:\.\d+)?cm\s+",
        "LA ",
        event_name,
        flags=re.IGNORECASE,
    )
    
    normalised = event_name.strip()

    
    
    
    return normalised
   




def calculate_personal_bests(performances):

    personal_bests = {}
    season_bests = {}

    

    grouped = {}

    for result in performances:
        if (
            "Javelin" in result.event_name
            or "Hurdles" in result.event_name
        ):
            event_name = normalise_event_name(
                result.event_name
            )

            

        if (
            result.performance_numeric is None
            or result.event_name is None
        ):
            continue

        if not is_legal_for_records(result):
            continue
        
        event_name = normalise_event_name(
            result.event_name
        )
        
        grouped.setdefault(
            event_name,
            []
        ).append(result)

    for event_name, event_results in grouped.items():

        field_keywords = [
            "Jump",
            "Vault",
            "Throw",
            "Discus",
            "Shot Put",
            "Javelin",
            "Hammer"
        ]

        is_field = any(
            keyword in event_name
            for keyword in field_keywords
        )

        #
        # Personal Best
        #

        if is_field:

            pb = max(
                event_results,
                key=lambda r: r.performance_numeric
            )

        else:

            pb = min(
                event_results,
                key=lambda r: r.performance_numeric
            )

        personal_bests[event_name] = pb

        #
        # Season Best
        #

        season_results = [

            r

            for r in event_results

            if is_current_season(
                r.competition_date
            )

        ]

        if season_results:

            if is_field:

                sb = max(
                    season_results,
                    key=lambda r: r.performance_numeric
                )

            else:

                sb = min(
                    season_results,
                    key=lambda r: r.performance_numeric
                )

            season_bests[event_name] = sb

    

    for event in sorted(personal_bests.keys()):
        
            
    

        return {

            "personal_bests": personal_bests,

            "season_bests": season_bests

    }


def parse_performance_numeric(
    performance: str,
    event_name: str
):
    """
    Convert performance strings into a sortable value.

    Track events:
        4:26.34 -> 266.34

    Field events:
        7.36 -> 7.36
    """

    if not performance:
        return None

    try:

        field_keywords = [
            "Jump",
            "Vault",
            "Throw",
            "Discus",
            "Shot Put",
            "Javelin",
            "Hammer"
        ]

        is_field = any(
            keyword in event_name
            for keyword in field_keywords
        )

        if is_field:
            return float(performance)

        #
        # Track
        #

        if ":" in performance:

            parts = performance.split(":")

            if len(parts) == 2:

                minutes = float(parts[0])

                seconds = float(parts[1])

                return (
                    minutes * 60
                    + seconds
                )

        return float(performance)

    except Exception:
        return None


 

def get_current_season():

    today = date.today()

    if today.month >= 10:
        return today.year

    return today.year - 1


def is_in_season(competition_date):

    if not competition_date:
        return False

    season_start_year = get_current_season()

    season_start = date(
        season_start_year,
        10,
        1
    )

    season_end = date(
        season_start_year + 1,
        4,
        30
    )

    return (
        season_start
        <= competition_date
        <= season_end
    )  