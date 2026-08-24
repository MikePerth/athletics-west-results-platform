import re
import pdfplumber

from collections import Counter

DEBUG = False

EVENT_PATTERN = re.compile(
    r"""
    ^
    (.*?)                      # event
    \s·\s
    (.*?)                      # category
    \s·\s
    (.*?)                      # division
    \s·\s
    (Final|Heat.*?|Semi.*?|Qualification)
    (?:\s·\sGroup\s([A-Z]))?
    """,
    re.VERBOSE,
)


NAME_PATTERN = re.compile(
    r"^(.*?)\s*(?:\([A-Z0-9,\s]+\)\s*)?\(\d{4}\)"
)


WIND_PATTERN = re.compile(
    r"Wind:\s*([+-]?\d+(?:\.\d+)?)"
)

YEAR_PATTERN = re.compile(
    r"\((19\d{2}|20\d{2})\)"
)

CLASSIFICATION_PATTERN = re.compile(
    r"\(([FT]\d+(?:,\s*[FT]\d+)*)\)"
)

COUNTRY_PATTERN = re.compile(
    r"\b(AUS|NZL|USA|GBR|GRE|RSA|JPN|CHN)\b"
)

RESULT_PATTERN = re.compile(
    r"^(\d+)\s+(.*?)\s+(\d+:\d+\.\d+|\d+\.\d+)\s*(PB|SB|DNS|DQ|DNF|NM|NH)?"
)

LANE_PATTERN = re.compile(
    r"^([0-9]+(?:-[0-9]+)?)\s+(.*)$"
)

AGE_GROUP_PATTERN = re.compile(
    r"\b(U\d+|Senior|M\d+|W\d+)\b"
)

TRACK_RESULT_PATTERN = re.compile(
    r"""
    ^
    (\d+)                  # place
    \s+
    (\d+(?:-\d+)?)         # lane
    \s+
    (.+?)                  # athlete block
    \s+
    ([0-9:]+\.[0-9]+)      # performance

    (?:\s+\([^)]+\))?      # optional countback

    \s*
    (PB|SB)?               # optional PB/SB

    (?:\s+([Qq]))?         # optional qualifier

    $
    """,
    re.VERBOSE
)

TRACK_RESULT_NO_LANE_PATTERN = re.compile(
    r"""
    ^
    (\d+)                    # place
    \s+
    (.+?)                    # athlete block
    \s+
    ([0-9:]+\.[0-9]+)        # performance
    \s*
    (PB|SB)?
    $
    """,
    re.VERBOSE,
)


TRACK_STATUS_PATTERN = re.compile(
    r"""
    ^
    (\d+(?:-\d+)?)         # lane
    \s+
    (.+?)                  # athlete block
    \s+
    (DNS|DNF|DQ)
    $
    """,
    re.VERBOSE
)


FIELD_RESULT_PATTERN = re.compile(
    r"""
    ^
    (\d+)                  # place
    \s+
    (.+?)                  # athlete block
    \s+
    (\d+\.\d+)             # performance

    (?:\s+(?:q|Q|QF|qf))?  # optional qualification marker

    (?:\s+(PB|SB))?        # optional PB/SB

    (?:\s+\([^)]+\))?      # optional secondary mark e.g. (6.56)

    (?:\s+([+-]\d+\.\d+))? # optional wind e.g. +1.7, -0.5

    (?:\s*NWI)?            # optional NWI

    $
    """,
    re.VERBOSE,
)

FIELD_STATUS_PATTERN = re.compile(
    r"""
    ^
    (.+?)
    \s+
    (NM|NH|DNS|DNF|DQ)
    $
    """,
    re.VERBOSE
)


RESULT_STATUSES = [
    "DNS",
    "DNF",
    "DQ",
    "NM",
    "NH"
]


RESULT_FLAGS = [
    "PB",
    "SB",
    "q",
    "Q",
    "DNS",
]



def normalise_category(category: str) -> str:
    category = category.strip()

    if category in {"Women & Girls", "Women", "Girls"}:
        return "Female"

    if category in {"Men & Boys", "Men", "Boys"}:
        return "Male"

   

def looks_like_field_result(line):

    return bool(
        re.match(
            r"^\d+\s+[A-Za-z]",
            line
        )
    )


def extract_club(text):

    age_group = extract_age_group(text)

    if not age_group:
        return None

    parts = text.split(age_group)

    if len(parts) < 2:
        return None

    return parts[1].strip()



def extract_age_group(text):

    match = AGE_GROUP_PATTERN.search(text)

    if match:
        return match.group(1)

    return None

def extract_lane_and_name(text):

    match = LANE_PATTERN.match(text)

    if match:
        return match.group(1), match.group(2)

    return None, text


def extract_birth_year(text):

    match = YEAR_PATTERN.search(text)

    if match:
        return int(match.group(1))

    return None


def extract_classification(text):

    match = CLASSIFICATION_PATTERN.search(text)

    if match:
        return match.group(1)

    return None



def extract_athlete_name(text):

    match = NAME_PATTERN.search(text)

    if match:
        return match.group(1).strip()

    return text.strip()


def extract_country(text):

    match = COUNTRY_PATTERN.search(text)

    if match:
        return match.group(1)

    return None


def extract_flag(text):

    if text.endswith("PB"):
        return "PB"

    if text.endswith("SB"):
        return "SB"

    return None


def extract_status(text):

    for status in RESULT_STATUSES:

        if text.endswith(status):
            return status

    return None


def extract_text(pdf_path: str) -> str:

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text



def is_place(value: str) -> bool:
    return value.isdigit()



def is_result(value: str) -> bool:

    if value in ["DNS", "DNF", "DQ"]:
        return True

    try:
        float(value)
        return True
    except:
        return False

def extract_club(text):

    country = extract_country(text)

    if not country:
        return None

    parts = text.split(country, 1)

    if len(parts) < 2:
        return None

    return parts[1].strip()


def parse_athlete_block(text):

    return {
        "athlete_name": extract_athlete_name(text),
        "birth_year": extract_birth_year(text),
        "classification": extract_classification(text),
        "country": extract_country(text),
        "club": extract_club(text),
        "status": None
    }



def parse_results_for_event(lines):

    results = []

    unparsed_count = 0

    for line in lines:

        line = line.strip()

        

        if line.startswith("Attempts"):
            break

        if "Attempts" in line:
            print(repr(line))
        

        if not line:
            continue

        if line.startswith("Place"):
            continue

        # Track results (with or without lanes)
        parsed = parse_track_result(line)

        if parsed:
            

            results.append(parsed)
            continue

        

        # Track statuses
        parsed = parse_track_status(line)

        if parsed:
            results.append(parsed)
            continue

        # Field results
        parsed = parse_field_result(line)

        if parsed:
            
            results.append(parsed)
            continue 

        

        # Field statuses
        parsed = parse_field_status(line)

        

        # Nothing matched

        unparsed_count += 1

    

    

    return results



def parse_roster_results(text: str):
    
    lines = text.splitlines()

    events = [] 
    current_event = None
    event_lines = []

    
    for line in lines:
        line = line.strip()

        if line.lstrip().startswith("Attempts"):

            if current_event:

                current_event["results"] = (
                    parse_results_for_event(event_lines)
                )

                for result in current_event["results"]:

                    if not result.get("age_group"):
                        result["age_group"] = (
                            extract_age_group(
                                current_event["division"]
                            )
                            or current_event["division"]
                        )

                current_event["result_count"] = len(
                    current_event["results"]
                )

                events.append(current_event)

            current_event = None
            event_lines = []

            continue

        event_match = EVENT_PATTERN.search(line)

        if event_match:

            # Save previous event
            if current_event:

                current_event["results"] = (
                    parse_results_for_event(event_lines)
                )

                for result in current_event["results"]:
                    

                    if not result.get("age_group"):

                        result["age_group"] = (
                            extract_age_group(
                                current_event["division"]
                            )
                            or current_event["division"]
                        )

                current_event["result_count"] = len(
                    current_event["results"]
                )

                events.append(current_event)
           

            
            wind_match = WIND_PATTERN.search(line)

            current_event = {
                "event": event_match.group(1),
                "category": normalise_category(
                    event_match.group(2)
                ),
                "division": event_match.group(3),
                "round": event_match.group(4),
                "group": event_match.group(5),
                "wind": (
                    float(wind_match.group(1))
                    if wind_match
                    else None
                ),
                "result_count": 0,
                "source_header": line,
                "results": []
            }

            

            event_lines = []

            continue

        
        
        if current_event:

            event_lines.append(line)

                           

            if wind_match:

                
                current_event["wind"] = float(
                    wind_match.group(1)
                )

    # Save final event
    if current_event:

        

        current_event["results"] = (
            parse_results_for_event(event_lines)
        )

        for result in current_event["results"]:
            

            if not result.get("age_group"):

                result["age_group"] = (
                    extract_age_group(
                        current_event["division"]
                    )
                    or current_event["division"]
                )

        

        current_event["result_count"] = len(
            current_event["results"]
        )

        events.append(current_event)

    

    # Summary statistics
    total_results = sum(
        len(event["results"])
        for event in events
    )

    

    #for event in events:
    #    for result in event["results"]:
    #        if result.get("age_group") == event["division"]:
    #            print(
    #                "MATCHED_DIVISION "
    #                f"EVENT={event['event']} "
    #                f"DIVISION={event['division']} "
    #                f"AGE={result['age_group']} "
    #                f"ATHLETE={result['athlete_name']}"
    #            )
    

   
    # Summary statistics
    total_results = sum(
        len(event["results"])
        for event in events
    )

    print(
        
        f"{len(events)} EVENTS FOUND "
        f"{total_results} RESULTS FOUND"
    )

    

    seen = {}

    for event in events:

        key = (
            event["event"],
            event["category"],
            event["division"],
            event["round"],
            event.get("group"),
        )

        if key in seen:
            #print("\nDUPLICATE EVENT:")
            #print("FIRST :", seen[key])
            #print("SECOND:", event["source_header"])

        #else:
            seen[key] = event["source_header"]

    return events



def parse_athlete_block(text):

    
    return {
        "athlete_name": extract_athlete_name(text),
        "birth_year": extract_birth_year(text),
        "classification": extract_classification(text),
        "country": extract_country(text),
        "age_group": extract_age_group(text),
        "club": extract_club(text),
        "status": None
    }



def parse_track_result(line):

    # Track events with lane numbers
    match = TRACK_RESULT_PATTERN.match(line)

    if match:

        place = int(match.group(1))
        lane = match.group(2)
        athlete_block = match.group(3)
        performance = match.group(4)
        roster_flag = match.group(5)

    else:

        # Track events without lanes (1500m, 3000m)
        match = TRACK_RESULT_NO_LANE_PATTERN.match(line)

        if not match:
            
            return None

        place = int(match.group(1))
        lane = None
        athlete_block = match.group(2)
        performance = match.group(3)
        roster_flag = match.group(4)

    

    athlete = parse_athlete_block(
        athlete_block
    )

    
    return {
        "place": place,
        "lane": lane,
        "athlete_name": athlete["athlete_name"],
        "birth_year": athlete["birth_year"],
        "classification": athlete["classification"],
        "country": athlete["country"],
        "age_group": athlete["age_group"],
        "club": athlete["club"],
        "performance": performance,
        "status": None,
        "roster_flag": roster_flag
    }



def parse_track_status(line):

    match = TRACK_STATUS_PATTERN.match(line)

    if not match:
        
        return None

    

    lane = match.group(1)

    athlete_block = match.group(2)

    status = match.group(3)

    athlete = parse_athlete_block(
        athlete_block
    )

   
    return {
        "place": None,
        "lane": lane,
        "athlete_name": athlete["athlete_name"],
        "birth_year": athlete["birth_year"],
        "classification": athlete["classification"],
        "country": athlete["country"],
        "age_group": athlete["age_group"],
        "club": athlete["club"],
        "performance": None,
        "roster_flag": None,
        "wind": None,
        "status": status
    }


def parse_field_result(line):

    match = FIELD_RESULT_PATTERN.match(line)

    if not match:

                
        return None

    place, athlete_block, performance, flag, wind = match.groups()

    
   

   
    club = extract_club(athlete_block)

    

    return {
        "place": int(place),
        "lane": None,
        "athlete_name": extract_athlete_name(
            athlete_block
        ),
        "birth_year": extract_birth_year(
            athlete_block
        ),
        "classification": extract_classification(
            athlete_block
        ),
        "country": extract_country(
            athlete_block
        ),
        "age_group": extract_age_group(
            athlete_block
        ),
        "club": extract_club(
            athlete_block
        ),
        "performance": performance,
        "status": None,
        "roster_flag": flag,
        "wind": (
            float(wind)
            if wind
            else None
        )
    }


def parse_field_status(line):

    match = FIELD_STATUS_PATTERN.match(line)

    if not match:
        
        return None

    

    athlete_block, status = match.groups()

    return {
        "place": None,
        "lane": None,
        "athlete_name": extract_athlete_name(
            athlete_block
        ),
        "birth_year": extract_birth_year(
            athlete_block
        ),
        "classification": extract_classification(
            athlete_block
        ),
        "country": extract_country(
            athlete_block
        ),
        "age_group": extract_age_group(
            athlete_block
        ),
        "club": extract_club(
            athlete_block
        ),
        "performance": None,
        "status": status,
        "roster_flag": None,
    }