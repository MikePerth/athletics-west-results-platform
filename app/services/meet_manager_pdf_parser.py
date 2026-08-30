import re
from app.services.gender_utils import (
    normalise_gender
) 

class MeetManagerPdfParser:

    def __init__(self):
        pass

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

        event_pattern = re.compile(
            r"Event\s+\d+.*?(?=Event\s+\d+|\Z)",
            re.DOTALL
        )

        matches = event_pattern.findall(text)

        for block in matches:

            event_number = self.extract_event_number(block)

            event_name = self.extract_event_name(block)

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

                #print("\n========================")
                #print("FIELD EVENT")
                #print(event_name)
                #print("========================")

                for line in block.splitlines()[:20]:
                    print(repr(line))

                athletes = self.parse_field_rows(
                    block.splitlines()
                )

            else:

                event_type = "track"

                #print("\n========================")
                #print("TRACK EVENT")
                #print(event_name)
                #print("========================")

                for line in block.splitlines()[:20]:
                    print(repr(line))

                athletes = self.parse_track_rows(
                    block.splitlines()
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

            key = (
                event["event_number"],
                event["event_name"]
            )

            if key not in merged_events:

                merged_events[key] = event

            else:

                merged_events[key]["athletes"].extend(
                    event["athletes"]
                )

        return list(
            merged_events.values()
)





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