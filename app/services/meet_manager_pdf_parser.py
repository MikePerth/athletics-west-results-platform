import re
from app.services.gender_utils import (
    normalise_gender
) 

class MeetManagerPdfParser:

    def __init__(self):
        pass

    def convert_two_digit_year(
        self,
        year_text
    ):

        year = int(year_text)

        if year <= 26:
            return f"20{year:02d}"

        return f"19{year:02d}"


    def clean_hytek_name(
        self,
        name
    ):

        name = re.sub(
            r"\s+[TF]\d+[A-Z]?",
            "",
            name
        )

        return name.strip()




    def normalise_hytek_name(
        self,
        name
    ):

        name = self.clean_hytek_name(
            name
        )

        #
        # Convert:
        # Surname, Firstname
        # ->
        # Firstname Surname
        #
        if "," in name:

            surname, firstname = (
                part.strip()
                for part in name.split(
                    ",",
                    1
                )
            )

            return (
                f"{firstname} {surname}"
            )

        return name
    

    def clean_hytek_result(
        self,
        result
    ):

        result = result.strip()

        #
        # World Championship Qualifier
        # 12.75W -> 12.75
        #
        if result.endswith("W"):
            result = result[:-1]

        #
        # Meet Record
        # 7:41.38M -> 7:41.38
        #
        if result.endswith("M"):
            result = result[:-1]

        return result


    def parse(self, text):

        events = self.extract_events(text)

        return events


    def extract_event_number(self, block):

        first_line = block.splitlines()[0]

        match = re.match(
            r"Event\s+(\d+)",
            first_line
        )

        if match:
            return int(match.group(1))

        return None


    def extract_events(self, text):

        events = []

        #
        # Existing Meet Manager parser
        # Event 1 ...
        # Event 2 ...
        #
        event_pattern = re.compile(
            r"Event\s+\d+.*?(?=Event\s+\d+|\Z)",
            re.DOTALL
        )

        matches = event_pattern.findall(text)

        print(
            f"EVENT-NUMBER BLOCKS FOUND = {len(matches)}"
        )

        #
        # Existing parser path
        #
        if matches:

            for block in matches:

                event_number = self.extract_event_number(
                    block
                )

                event_name = self.extract_event_name(
                    block
                )

                gender = normalise_gender(
                    event_name
                )

                if any(
                    keyword in event_name
                    for keyword in [
                        "Long Jump",
                        "Triple Jump",
                        "High Jump",
                        "Pole Vault",
                        "Shot Put",
                        "Discus",
                        "Hammer",
                        "Javelin"
                    ]
                ):

                    event_type = "field"

                    athletes = (
                        self.parse_field_rows(
                            block.splitlines()
                        )
                    )

                else:

                    event_type = "track"

                    athletes = (
                        self.parse_track_rows(
                            block.splitlines()
                        )
                    )

                events.append(
                    {
                        "event_number": event_number,
                        "event_name": event_name,
                        "event_type": event_type,
                        "gender": gender,
                        "athletes": athletes
                    }
                )

            merged_events = {}

            for event in events:

                print(
                    f"{event['event_name']}: "
                    f"{len(event['athletes'])} athletes"
                )

                key = (
                    event["event_number"],
                    event["event_name"]
                )

                if key not in merged_events:

                    merged_events[key] = event

                else:

                    merged_events[key][
                        "athletes"
                    ].extend(
                        event["athletes"]
                    )

            return list(
                merged_events.values()
            )

        #
        # Fallback parser for Hy-Tek exports
        # Example:
        # Women 100 Metres
        # Men 200 Metres
        #
        print(
            "NO EVENT-NUMBER EVENTS FOUND"
        )

        print(
            "ATTEMPTING HY-TEK FALLBACK PARSER"
        )

        return self.extract_hytek_events(
            text
        )


    def extract_hytek_events(
        self,
        text
    ):

        print(
            "HY-TEK FALLBACK PARSER ACTIVATED"
        )

        events = []

        lines = text.splitlines()

        #
        # Event headers like:
        #
        # Women 100 Metres
        # Men 200 Metres
        # Women Long Jump
        #
        header_pattern = re.compile(
            r"^(Women|Men)\s+.+$"
        )

        event_headers = []

        for i, line in enumerate(lines):

            line = line.strip()

            if not line:
                continue

            #
            # Ignore page headers
            #
            if (
                "MEET MANAGER" in line
                or "Results" == line
                or "Athletics House" in line
            ):
                continue

            if header_pattern.match(line):

                event_headers.append(
                    (i, line)
                )

        print(
            f"HY-TEK HEADERS FOUND = "
            f"{len(event_headers)}"
        )

        for idx, (start_idx, header) in enumerate(
            event_headers
        ):

            if idx < len(event_headers) - 1:

                end_idx = (
                    event_headers[idx + 1][0]
                )

            else:

                end_idx = len(lines)

            block_lines = (
                lines[start_idx:end_idx]
            )

            block_text = "\n".join(
                block_lines
            )

            event_name = header.strip()

            if event_name == "Women Long Jump":

                print("\n===================")
                print("WOMEN LONG JUMP")
                print("===================")

                for line in block_lines:
                    print(repr(line))

                print("===================\n")

            if event_name == "Men Long Jump":

                print("\n===================")
                print("MEN LONG JUMP")
                print("===================")

                for line in block_lines:
                    print(repr(line))

                print("===================\n")

            #if event_name == "Women 1500 Metres":

            #    print("\n===================")
            #    print("WOMEN 1500 METRES")
            #    print("===================")

            #    for line in block_lines:
            #        print(repr(line))

            #    print("===================\n")

            gender = normalise_gender(
                event_name
            )

            if any(
                keyword in event_name
                for keyword in [
                    "Long Jump",
                    "Triple Jump",
                    "High Jump",
                    "Pole Vault",
                    "Shot Put",
                    "Discus",
                    "Hammer",
                    "Javelin"
                ]
            ):

                event_type = "field"

                athletes = (
                    self.parse_hytek_field_rows(
                        block_lines
                    )
                )

                if len(athletes) == 0:

                    print(
                        "\n=============================="
                    )
                
                    print(
                        f"NO ATHLETES EXTRACTED: "
                        f"{event_name}"
                    )
                
                    print(
                        "==============================\n"
                    )
            

            else:

                event_type = "track"

                athletes = (
                    self.parse_hytek_track_rows(
                        block_lines
                    )
                )
            
                
                for athlete in athletes:

                    if not self.is_valid_performance(
                        athlete.get("result")
                    ):

                        print(
                            "\n=============================="
                        )

                        print(
                            "INVALID PERFORMANCE"
                        )

                        print(
                            f"EVENT: {event_name}"
                        )

                        print(
                            athlete
                        )

                        print(
                            "==============================\n"
                        )
                
            events.append(
                {
                    "event_number": None,
                    "event_name": event_name,
                    "event_type": event_type,
                    "gender": gender,
                    "athletes": athletes
                }
            )

        print(
            f"HY-TEK EVENTS PARSED = "
            f"{len(events)}"
        )

        return events



    def is_valid_performance(
        self,
        result
    ):

        if result is None:
            return False

        result = str(result).strip()

        #
        # Numeric field event
        # 6.72
        # 59.00
        #
        if re.match(
            r"^\d+\.\d+$",
            result
        ):
            return True

        #
        # Track time
        # 11.20
        # 1:45.85
        # 4:07.11
        #
        if re.match(
            r"^\d+(?::\d+)*(?:\.\d+)?$",
            result
        ):
            return True

        return False

    def normalise_club_name(
        self,
        club
    ):

        club_map = {

            "Athletics We": "AW Independent",

            "Perth Track": "PTF",

            "Uwa Athletic": "UWA",

            "Curtin Unive": "Curtin University",

            "Kingsway Ath": "Kingsway Athletics",

            "Melville Roa": "Melville Roar",

            "Belmont Athl": "Belmont Athletics",

            "Inglewood At": "Inglewood Athletics",

            "Joondalup At": "Joondalup Athletics",

            "Bunbury Regi": "Bunbury Regional Athletics Club",

            "Canning Dist": "Canning Districts",

            "Ridgewood At": "Ridgewood Athletics",

            "Tracksters A": "Tracksters Athletics",

            "Mandurah Roc": "Mandurah Rockingham",

            "Cockburn Ath": "Cockburn Athletics",

            "Hamersley At": "Hamersley Athletics",

            "West Track Club": "West Track Club",

            "Canning Dist": "Canning Districts",

            "Masters Athl": "Masters Athletics",

            "North Beach": "North Beach",

            "Dale Athleti": "Dale Athletics"
        }

        if club not in club_map:
            print(
                f"UNMAPPED CLUB: '{club}'"
            )

            return club
        
        return club_map[club]
            


    def parse_hytek_track_rows(
        self,
        lines
    ):

        athletes = []

        result_pattern = re.compile(
            r"^\s*(\d+)\s+"
            r"(.+?)\s+"
            r"(\d{2})\s+"
            r"([A-Z]{3})\s+"
            r"([\d:.]+)\s+"
            r"(-?\d+\.\d+)\s*$"
        )

        distance_pattern = re.compile(
            r"^\s*(\d+)\s+"
            r"(.+?)\s+"
            r"(\d{2})\s+"
            r"([A-Z]{3})\s+"
            r"([\d:.]+)"
            r"(?:\s+.*)?$"
        )

        for line in lines:

            line = line.strip()

            #if (
            #    line.startswith("1 ")
            #    or line.startswith("2 ")
            #    or line.startswith("3 ")
            #):
                #print(
                #    "TRACK LINE:",
                #    repr(line)
                #)

            match = result_pattern.match(
                line
            )

            if not match:

                match = distance_pattern.match(
                    line
                )

            if not match:
                continue

            year = int(
                match.group(3)
            )

            if year <= 26:
                birth_year = (
                    f"20{year:02d}"
                )
            else:
                birth_year = (
                    f"19{year:02d}"
                )

            athletes.append(
                {
                    "place": match.group(1),
                    "name": self.normalise_hytek_name(
                        match.group(2)
                    ),
                    "birth_year": self.convert_two_digit_year(
                        match.group(3)
                    ),
                    "country": match.group(4),
                    "result": self.clean_hytek_result(
                        match.group(5)
                    ),
                    "status": None
                }
            )

        return athletes


    def parse_hytek_field_rows(
        self,
        lines
    ):

        athletes = []

        result_pattern = re.compile(
            r"^\s*(\d+)\s+"
            r"(.+?)\s+"
            r"(\d{2})\s+"
            r"([A-Z]{3})\s+"
            r"([\d.]+m?)"
            r"(?:\s+[+-]?\d+\.\d+)?\s*$"
        )

        for line in lines:

            match = result_pattern.match(
                line.strip()
            )

            if not match:
                continue

            athletes.append(
                {
                    "place": match.group(1),
                    "name": self.normalise_hytek_name(
                        match.group(2)
                    ),
                    "birth_year": (
                        self.convert_two_digit_year(
                            match.group(3)
                        )
                    ),
                    "country": match.group(4),
                    "result": (
                        match.group(5)
                        .rstrip("m")
                    ),
                    "status": None
                }
            )

        return athletes







    def extract_event_name(self, block):

        first_line = block.splitlines()[0]

        return re.sub(
            r"^Event\s+\d+\s+",
            "",
            first_line
        ).strip(" .")



    

    def parse_track_rows(self, rows):

        athletes = []

        current_wind = None

        for row in rows:

            row = row.strip()

            if not row:
                continue

            if row.startswith("Event "):
                continue

            if row.startswith("Section"):
                continue

            if "MEET MANAGER" in row:
                continue

            if "Site License" in row:
                continue

            if row.startswith("="):
                continue

            if row.startswith("Name"):
                continue

            wind_match = re.search(
                r"Wind:\s*([+-]?\d+(?:\.\d+)?)",
                row
            )

            if wind_match:

                current_wind = float(
                    wind_match.group(1)
                )

                continue            

            print(f"TRACK ROW: {row}")
            
            athlete = self.parse_track_row(
                row,
                current_wind
            )

            if athlete:

                athletes.append(
                    athlete
                )

        return athletes






    def parse_track_row(
        self,
        row,
        wind
    ):

        match = re.match(
            r"^\s*(\d+|--)\s+(?:#\s*\d+\s+)?(.*?)\s+(\d{2})\s+(.+?-[A-Z]{2,3})\s+([\d:\.]+)(?:\s+.*)?$",
            row
        )

        if not match:

            row_stripped = row.strip()

            # Only log rows that look like athlete result rows
            if re.match(
                r"^\d+\s+#",
                row_stripped
            ):

                print(
                    f"TRACK PARSE FAILURE: {row}"
                )

            return None
        

        place = int(
            match.group(1)
        )

        name = match.group(2)

        #
        # Remove Meet Manager bib numbers
        #
        # #100 Emma Kempson
        # # 100 Emma Kempson
        #
        name = re.sub(
            r"^#\s*\d+\s+",
            "",
            name
        ).strip()

        name = name.title()

        name = re.sub(
            r"\s+[TF]\d{2,}$",
            "",
            name
        )

        year = int(match.group(3))
        
        if year <= 30:
            birth_year = 2000 + year
        else:
            birth_year = 1900 + year

        team = match.group(4)

        result = match.group(5)

        club, country = team.rsplit(
            "-",
            1
        )

        club = self.normalise_club_name(
            club.strip()
        )

        




        return {
            "place": place,
            "name": name,
            "birth_year": birth_year,
            "club": club.strip(),
            "country": country.strip(),
            "result": result,
            "wind": wind,
            "status": None,
            "raw_row": row
        }




    def parse_field_rows(self, rows):

        athletes = []

        current_flight = None

        for row in rows:

            row = row.strip()

            if not row:
                continue

            if row.startswith("Flight"):

                current_flight = row

                continue

            print(
                f"FIELD ROW: {row}"
            )

            athlete = self.parse_field_row(
                row,
                current_flight
            )

            if athlete:

                athletes.append(
                    athlete
                )

        return athletes





    def parse_field_row(
        self,
        row,
        flight
    ):

        if not re.match(
            r"^\s*(\d+|--)\s+",
            row
        ):
            return None

        match = re.match(
            r"^\s*(\d+|--)\s+(?:#\s*\d+\s+)?(.*?)\s+(\d{2})\s+(.+?-([A-Z]{3}))\s+([J]?[\d\.]+)m(?:\s+(Retired|NWI|[+-]?\d+\.\d+))?\s*$",
            row
        )

        if not match:

            row_stripped = row.strip()

            if re.match(
                r"^\d+\s+#",
                row_stripped
            ):

                print(
                    f"FIELD PARSE FAILURE: {row}"
                )

            return None

        place = int(
            match.group(1)
        )

        name = match.group(2)

        #
        # Remove Meet Manager bib numbers
        #
        # #100 Emma Kempson
        # # 100 Emma Kempson
        #
        name = re.sub(
            r"^#\s*\d+\s+",
            "",
            name
        ).strip()

        name = name.title()

        name = re.sub(
            r"\s+[TF]\d{2,}$",
            "",
            name
        )

        year = int(match.group(3))

        if year <= 30:
            birth_year = 2000 + year
        else:
            birth_year = 1900 + year

        team = match.group(4)

        result = match.group(6)

        club, country = team.rsplit(
            "-",
            1
        )

        club = self.normalise_club_name(
            club.strip()
        )

        

        status = None

        wind = match.group(7)

        if wind == "NWI":
            wind = None

        elif wind == "Retired":
            status = "Retired"
            wind = None

        elif wind:
            wind = float(wind)

        else:
            wind = None

               
        
        return {
            "place": place,
            "name": name,
            "birth_year": birth_year,
            "club": club.strip(),
            "country": country.strip(),
            "result": result,
            "wind": wind,
            "group_name": flight,
            "status": None,
            "raw_row": row
        }