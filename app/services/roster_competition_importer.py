from playwright.sync_api import sync_playwright
from pprint import pprint
import time
import re
import json 
import os
import traceback

from app.services.gender_utils import (
    normalise_gender
)


class LayoutType:

    TRACK_STANDARD = "track_standard"

    TRACK_NOTES = "track_notes"

    TRACK_NOTES_AGEGROUP = (
        "track_notes_agegroup"
    )

    TRACK_COMPACT_NOTES = (
        "track_compact_notes"
    )

    TRACK_AGEGROUP_DETAILS = (
        "track_agroup_details"
    )

    TRACK_COMPACT_NO_BIRTHYEAR = (
        "track_compact_no_birthyear"
    )

    TRACK_STEEPLECHASE = (
        "track_steeplechase"
    )

    
    FIELD_STANDARD = "field_standard"

    FIELD_AGEGROUP_IMPLEMENT = (
        "field_agegroup_implement"
    )

    FIELD_PARA_PERCENTAGE = (
        "field_para_percentage"
    )

    FIELD_NOTES_AGEGROUP_IMPLEMENT = (
        "field_notes_agegroup_implement"
    )

    FIELD_NOTES_CLUB_RESULT = (
        "field_notes_club_result"
    )
    
    


class RosterCompetitionImporter:

    def __init__(
        self,
        competition_url
    ):

        
        self.competition_url = (
            competition_url
        )


    def detect_track_layout(
        self,
        record
    ):

        #
        # Original steeplechase format
        #
        if (
            len(record) >= 10
            and record[2] in ["M", "F"]
        ):
            return LayoutType.TRACK_STEEPLECHASE
        #
        # International compact notes format
        #
        # GBR
        # Notes: Hip 11
        # Senior    Nottingham    2:26.21
        #
        if (
            len(record) == 6
            and len(record[2]) == 3
            and record[3].startswith("Notes:")
        ):
            return LayoutType.TRACK_COMPACT_NOTES
        #
        # Notes:
        # U18
        # 83.8cm / 35m    Club    56.21
        #
        if (
            len(record) > 7
            and str(record[5]).startswith("Notes:")
            and re.match(
                r"^(U\d+|U23|Senior|Open)$",
                str(record[6])
            )
        ):
            return (
                LayoutType
                .TRACK_NOTES_AGEGROUP
            )

        #
        # No birth year
        #
        if (
            len(record) in [4, 5]
            and len(record[2]) == 3
            and "\t" in record[3]
        ):
            return LayoutType.TRACK_COMPACT_NO_BIRTHYEAR



        #
        # Notes:
        # Senior    UWA    14:45.32
        #
        if (
            len(record) > 6
            and str(record[5]).startswith("Notes:")
        ):
            return (
                LayoutType
                .TRACK_NOTES
            )

        #
        # U15
        # 76.2cm / 18.29m    PTFC    29.51
        #
        # Senior
        # 91.4cm / 35m    UWA    52.54
        #
        if (
            len(record) > 6
            and re.match(
                r"^(U\d+|U23|Senior|Open)$",
                str(record[5])
            )
        ):
            return (
                LayoutType
                .TRACK_AGEGROUP_DETAILS
            )

        return (
            LayoutType
            .TRACK_STANDARD
        )


    def parse_track_compact_notes(
        self,
        record
    ):

        country = record[2]

        details_parts = (
            record[4]
            .split("\t")
        )

        age_group = None
        club = None
        result = None

        if len(details_parts) >= 3:

            age_group = details_parts[0]

            club = details_parts[1]

            result = details_parts[2]

        return (
            country,
            age_group,
            club,
            result
        )                               


    def parse_track_compact_no_birthyear(
        self,
        record
    ):
        birth_year = None

        country = record[2]

        details_parts = (
            record[3]
            .split("\t")
        )

        age_group = None
        club = None
        result = None

        if len(details_parts) >= 3:

            age_group = details_parts[0]
            club = details_parts[1]
            result = details_parts[2]

        elif len(details_parts) == 2:

            club = details_parts[0]
            result = details_parts[1]

        return (
            birth_year,
            country,
            age_group,
            club,
            result
        )


    

    def parse_track_agroup_details(
        self,
        record
    ):

        age_group = record[5]

        details_parts = (
            record[6]
            .split("\t")
        )

        club = None

        result = None

        if len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )
    
    def parse_track_standard(
        self,
        record
        ):

            
        details_parts = (
            record[5]
            .split("\t")
        )

        age_group = None

        club = None

        result = None

        if len(details_parts) == 1:

            result = details_parts[0]

        elif len(details_parts) == 2:

            club = details_parts[0]

            result = details_parts[1]

        elif len(details_parts) >= 3:

            age_group = details_parts[0]

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )           
    
    def parse_track_steeplechase(
        self,
        record
    ):

        birth_year = record[4]

        country = record[6]

        age_group = record[8]

        details_parts = (
            record[9]
            .split("\t")
        )

        club = None

        result = None

        if len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            birth_year,
            country,
            age_group,
            club,
            result
        )


    def parse_track_notes_agegroup(
        self,
        record
    ):

        age_group = record[6]

        details_parts = (
            record[7]
            .split("\t")
        )

        club = None

        result = None

        if len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )
    
    def parse_track_notes(
        self,
        record
    ):

        details_parts = (
            record[6]
            .split("\t")
        )

        details_parts = [
            part.strip()
            for part in details_parts
        ]

        age_group = None
        club = None
        result = None

        if len(details_parts) == 1:

            result = details_parts[0]

        elif len(details_parts) == 2:

            club = details_parts[0]
            result = details_parts[1]

        elif len(details_parts) == 3:

            age_group = details_parts[0]

            club = details_parts[1]

            result = details_parts[2]

        elif len(details_parts) >= 4:

            age_group = details_parts[0]

            #
            # Para XC format:
            # PA Senior\t860\t\t9:04
            #
            result = details_parts[-1]
        else:

            print(
                f"UNHANDLED TRACK_NOTES: {record}"
            )

        return (
            age_group,
            club,
            result
        )



    def extract_special_road_rows(
        self,
        text
    ):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        start = None

        for i, line in enumerate(lines):

            if "PARTICIPANT" in line:

                start = i + 1
                break

        if start is None:
            return []

        end = len(lines)

        for i in range(start, len(lines)):

            if lines[i] == "Metric":

                end = i
                break

            data = lines[start:end]

            for i, line in enumerate(data):

                if re.match(
                    r"^\d+\t-$",
                    line
                ):
                    data[i] = line.replace(
                        "\t-",
                        "\t0"
                    )

            return data

        return lines[start:end]


    
    def parse_track_agegroup_details(
        self,
        record
    ):

        age_group = record[5]

        details_parts = (
            record[6]
            .split("\t")
        )

        club = None
        result = None

        if len(details_parts) >= 3:

            club = details_parts[-2]
            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )



    def detect_field_layout(
        self,
        record
    ):

       

        #
        # Para field event
        #
        if (
            len(record) > 6
            and str(record[5]).startswith("Notes:")
            and "%" in str(record[5])
            and "\t" in str(record[6])
        ):

            print(
                "LAYOUT =>",
                LayoutType.FIELD_PARA_PERCENTAGE
            )

            return (
                LayoutType
                .FIELD_PARA_PERCENTAGE
            )

        #
        # Notes:
        # 600g
        # U18
        # 500g    UWA    35.85
        #
        if (
            len(record) > 7
            and str(record[5]).startswith("Notes:")
            and re.match(
                r"^(U\d+|U23|Senior|Open)$",
                str(record[6])
            )
        ):

            

            return (
                LayoutType
                .FIELD_NOTES_AGEGROUP_IMPLEMENT
            )

        #
        # U14
        # 400g    Club    45.12
        #
        if (
            len(record) > 6
            and re.match(
                r"^(U\d+|U23|Senior|Open)$",
                str(record[5])
            )
        ):

            

            return (
                LayoutType
                .FIELD_AGEGROUP_IMPLEMENT
            )

        

        #
        # Notes field present
        # Club + Result moved to next column
        #
        if (
            len(record) > 6
            and str(record[5]).startswith(
                "Notes:"
            )
        ):

            return (
                LayoutType
                .FIELD_NOTES_CLUB_RESULT
            )

        return (
            LayoutType
            .FIELD_STANDARD
        )






    def parse_field_notes_club_result(
        self,
        record
    ):

        age_group = None

        club = None

        result = None

        details_parts = (
            record[6]
            .split("\t")
        )

        if len(details_parts) >= 2:

            club = (
                details_parts[0]
            )

            result = (
                details_parts[1]
            )

        elif len(details_parts) == 1:

            result = (
                details_parts[0]
            )

        

        return (
            age_group,
            club,
            result
        )
           



    def parse_field_standard(
        self,
        record
    ):

        details_parts = (
            record[5]
            .split("\t")
        )

        age_group = None

        club = None

        result = None

        if len(details_parts) == 1:

            result = details_parts[0]

        elif len(details_parts) == 2:

            club = details_parts[0]

            result = details_parts[1]

        elif len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )


    def parse_field_agegroup_implement(
        self,
        record
    ):

        age_group = record[5]

        details_parts = (
            record[6]
            .split("\t")
        )

        club = None

        result = None

        status = None

        if len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

            
        return (
            age_group,
            club,
            result
        )


    def parse_field_para_percentage(
        self,
        record
    ):

        details_parts = (
            record[6]
            .split("\t")
        )

        age_group = None
        club = None
        result = None

        if len(details_parts) >= 3:

            age_group = details_parts[0]
            club = details_parts[1]
            result = details_parts[2]

        elif len(details_parts) == 2:

            club = details_parts[0]
            result = details_parts[1]

            return (
                age_group,
                club,
                result
            )

    

    def import_competition(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                self.competition_url,
                wait_until="networkidle"
            )

            print(
                f"Accept buttons: {page.get_by_text('Accept').count()}"
            )

            if page.get_by_text("Accept").count() > 0:

            
                    page.get_by_text(
                        "Accept",
                        exact=True
                    ).click()

                    print("Accepted cookies")

                    page.wait_for_timeout(1000)

                


            switch_button = page.get_by_role(
                "button",
                name="Switch"
            )
            
            if switch_button.count() == 0:

                print(
                    "Roster layout without Switch detected"
                )

            else:

                try:

                    switch_button.first.click()

                    page.wait_for_timeout(1000)

                    print(
                        "Switched to results view"
                    )

                except Exception as e:

                    print(
                        f"Unable to click Switch: {e}"
                    )
            

            page.locator(
                ".event-name"
            ).first.wait_for(timeout=10000)

            event_count = page.locator(
                ".event-name"
            ).count()

            print(
                f"Found {event_count} events"
            )

            all_events = []

            failed_events =[]

            failed_records = 0

            unhandled_records = 0

            # Test first 3 events only

            for i in range(event_count):

                event_elements = page.locator(
                    ".event-name"
                )

                event_name = (
                    event_elements
                    .nth(i)
                    .inner_text()
                )
                

                

                print(
                    f"Loading event {i}: {event_name}"
                )

                event_elements.nth(i).click()

                page.wait_for_timeout(2000)
                
                event_data = self.extract_event(
                    page
                )
                

                gender = normalise_gender(
                    event_data.get("event_details")
                )

                event_data["gender"] = gender

                

                round_name = None

                if "·" in event_name:

                    round_text = (
                        event_name
                        .split("·", 1)[1]
                        .strip()
                    )

                    if round_text.startswith("Heat"):
                        round_name = "Heat"

                    elif round_text.startswith("Semi"):
                        round_name = "Semi"

                    elif round_text.startswith("Final"):
                        round_name = "Final"

                event_data["round"] = round_name

                print(
                    f"event_type={event_data['event_type']}"
                )

                print(
                    f"ROUND DETECTED: {event_name} -> {round_name}"
                )

                try:

                    if event_data["event_type"] == "field":

                        athletes = self.parse_field_rows(
                            event_data["rows"]
                        )

                    elif event_data["event_type"] == "track":

                        
                        athletes = self.parse_track_rows(
                            event_data["rows"]
                        )

                    else:

                        athletes = []

                except Exception as e:

                    print(
                        f"Failed event: {event_data['event_name']}"
                    )

                    print(
                        traceback.format_exc()
                    )

                    failed_events.append(
                        {
                            "event": event_data["event_name"],
                            "rows": len(event_data["rows"]),
                            "error": str(e)
                        }
                    )

                    athletes = []

                    failed_records += len(
                        event_data["rows"]
                    )

                event_data["athletes"] = athletes
                event_data.pop("rows", None)
                all_events.append(event_data)

                switch_button = page.get_by_role(
                    "button",
                    name="Switch"
                )

                if switch_button.count() > 0:

                    switch_button.first.click()

                    page.wait_for_timeout(1000)               

                 
            print("\nEVENT TYPE CHECK")

            for i, event in enumerate(all_events):

                if not isinstance(event, dict):

                    print(
                        f"BAD EVENT AT INDEX {i}"
                    )

                    

            athlete_count = sum(
                len(event["athletes"])
                for event in all_events
                if isinstance(event, dict)
            )

            missing_results = 0

            for event in all_events:

                for athlete in event["athletes"]:

                    if (
                        not athlete.get("result")
                        and athlete.get("status") is None
                    ):

                        print(
                            f"\nMISSING RESULT | "
                            f"{event['event_name']} | "
                            f"{athlete['name']}"
                        )

                        for i, value in enumerate(
                            athlete["source_record"]
                        ):
                            print(
                                f"{i}: {repr(value)}"
                            )

           

            
            
            print("\n===================")
            print("IMPORT SUMMARY")
            print("===================")

            print(f"Events: {len(all_events)}")
            print(f"Athletes: {athlete_count}")
            print(f"Failed records: {failed_records}")
            print(f"Unhandled records: {unhandled_records}")
            print(f"Missing results: {missing_results}")

            

            print("===================\n")

            browser.close()

            

            return all_events



             
    def parse_field_notes_agegroup_implement(
        self,
        record
    ):

        age_group = record[6]

        details_parts = (
            record[7]
            .split("\t")
        )

        club = None
        result = None

        if len(details_parts) >= 3:

            club = details_parts[-2]

            result = details_parts[-1]

        return (
            age_group,
            club,
            result
        )




    def parse_event_list(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        try:
            start = lines.index("Events") + 1
        except ValueError:
            return []

        events = []

        i = start

        while i < len(lines):

            # skip date headings
            if re.match(
                r"\d{2}/\d{2}/\d{4}",
                lines[i]
            ):
                i += 1
                continue

            # event block always begins with a time
            if re.match(
                r"\d{1,2}:\d{2}\s*[AP]M",
                lines[i]
            ):

                event = {
                    "time": lines[i]
                }

                block = []

                i += 1

                while (
                    i < len(lines)
                    and not re.match(
                        r"\d{1,2}:\d{2}\s*[AP]M",
                        lines[i]
                    )
                ):

                    block.append(lines[i])
                    i += 1

                event["details"] = block

                events.append(event)

                continue

            i += 1

        return events



    
    
    def extract_rows(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        start = None

        for i, line in enumerate(lines):

            if "PARTICIPANT" in line:

                start = i + 1
                break

        if start is None:
            return []

        end = len(lines)

        for i in range(start, len(lines)):

            if lines[i] == "Metric":

                end = i
                break

        return lines[start:end]




    
    def save_event(self, event_data):

        print(
            f"Saving {event_data['event_name']}"
        )

        # TODO:
        # Insert into database





    def get_event_names(self, page):

        page.get_by_role(
            "button",
            name="Switch"
        ).click()

        time.sleep(1)

        text = page.locator(
            "body"
        ).inner_text()

        return self.parse_event_list(
            text
        )


    


    def load_event(
        self,
        page,
        event_name
    ):

        page.get_by_role(
            "button",
            name="Switch"
        ).click()

        time.sleep(1)

        page.get_by_text(
            event_name,
            exact=True
        ).click()

        time.sleep(2)





    def extract_event(self, page):

        


        text = page.locator(
            "body"
        ).inner_text()

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]
        


        try:

            participants_index = lines.index(
                "Participants"
            )

            event_name = lines[
                participants_index + 1
            ]

            event_details = lines[
                participants_index + 2
            ]


            field_keywords = {
                "Long Jump",
                "Triple Jump",
                "High Jump",
                "Pole Vault",
                "Shot Put",
                "Discus",
                "Javelin",
                "Hammer",
            }

            event_type = "track"

            if any(
                keyword in event_name
                for keyword in field_keywords
            ):
                event_type = "field"

            

        except ValueError:

            event_name = None
            event_details = None

        
        if "id=25926" in self.competition_url:

            

            rows = self.extract_special_road_rows(
                text
            )

        else:

            rows = self.extract_rows(
                text
            )

        return {
            "event_name": event_name,
            "event_details": event_details,
            "wind": self.extract_wind(text),
            "event_type": event_type,
            "rows": rows
        }
        
        #return {
        #    "event_name": event_name,
        #    "event_details": event_details,
        #    "wind": self.extract_wind(text),
        #    "event_type": event_type,
        #    "rows": self.extract_rows(text)
        #}


    


    def extract_wind(
        self,
        text
    ):

        match = re.search(
            r"Wind:\s*([+-]?\d+(?:\.\d+)?)",
            text
        )

        return (
            float(match.group(1))
            if match
            else None
        )





    def parse_results(self, event_data):

        rows = event_data["rows"]

        if event_data["event_type"] == "field":
            return self.parse_field_rows(rows)

        return self.parse_track_rows(rows)



    

    def parse_field_rows(self, rows):

        current_record = []

        records = []

        # build records
        for row in rows:

            if self.is_field_record_start(row):

                if current_record:
                    records.append(current_record)

                current_record = [row]

            else:
                current_record.append(row)

        if current_record:
            records.append(current_record)

        athletes = []

        for record in records:

            
            place = None
            order = None
            age_group = None
            club = None
            result = None
            status = None

            parts = record[0].split("\t")

            if len(parts) == 2:
                place = parts[0]
                order = parts[1]
            else:
                place = record[0]

            

            if len(record) < 6:

                print(
                    f"SHORT FIELD RECORD: {record}"
                )

                continue

            

            layout = self.detect_field_layout(
                record
            )

            

            if (
                layout
                == LayoutType.FIELD_STANDARD
            ):

                (
                    age_group,
                    club,
                    result
                ) = self.parse_field_standard(
                    record
                )

            elif (
                layout
                == LayoutType.FIELD_AGEGROUP_IMPLEMENT
            ):

                (
                    age_group,
                    club,
                    result
                ) = (
                    self.parse_field_agegroup_implement(
                        record
                    )
                )


            elif (
                layout
                == LayoutType.FIELD_PARA_PERCENTAGE
            ):

                (
                    age_group,
                    club,
                    result
                ) = self.parse_field_para_percentage(
                    record
                )

            elif (
                layout
                == LayoutType.FIELD_NOTES_AGEGROUP_IMPLEMENT
            ):

                (
                    age_group,
                    club,
                    result
                ) = (
                    self.parse_field_notes_agegroup_implement(
                        record
                    )
                )

            elif (
                layout
                == LayoutType.FIELD_NOTES_CLUB_RESULT
            ):

                (
                    age_group,
                    club,
                    result
                ) = (
                    self.parse_field_notes_club_result(
                        record
                    )
                ) 


            


            else:

                print(
                    f"UNKNOWN FIELD LAYOUT: {record}"
                )

                continue
            
            wind = None

            


            if result:

                wind_match = re.search(
                    r"\((NWI|[+-]?\d+(?:\.\d+)?)\)$",
                    result.strip()
                )

                if wind_match:

                    wind = wind_match.group(1)

                    if wind == "NWI":
                        wind = None

                    result = re.sub(
                        r"\s*\((NWI|[+-]?\d+(?:\.\d+)?)\)$",
                        "",
                        result
                    ).strip()


            name = record[1]

            if result in [
                "DNS",
                "DQ",
                "NM",
                "DNF"
            ]:
                status = result          

            name = name.replace("\xa0", " ")

            if "·" in name:
                name = name.split("·")[0].strip()

            name = name.title()

           

            if not result and not status:

                print("\n==============================")
                print("UNHANDLED FIELD RECORD")
                print("==============================")
                print(f"LAYOUT: {layout}")
                print(f"NAME: {record[1]}")
                print(f"RECORD LENGTH: {len(record)}")

                for i, value in enumerate(record):
                    print(f"{i}: {repr(value)}")

                print("==============================\n")

            athlete = {

                "place": place,
                "order": order,
                "name": name,
                "birth_year": record[2],
                "country": record[4],
                "age_group": age_group,
                "club": club,
                "result": result,
                "wind": wind,
                "status": status,
                "source_record": record

            }

            athletes.append(athlete)

        return athletes




    def parse_track_rows(self, rows):
        

        current_record = []

        records = []

        unhandled_records = 0

        for row in rows:

            if self.is_track_record_start(row):

                if current_record:

                    records.append(
                        current_record
                    )

                current_record = [row]

            else:

                current_record.append(row)

        if current_record:

            records.append(current_record)


        athletes = []

        for record in records:

            try:

            
                place = None
                lane = None
                age_group = None
                club = None
                result = None
                status = None
                birth_year = None

                parts = record[0].split("\t")

                if len(parts) == 2:
                    place = parts[0]
                    lane = parts[1]
                else:
                    place = record[0]
            

                if len(record) > 2:

                    candidate = record[2].strip()

                    if re.fullmatch(r"\d{4}", candidate):

                        birth_year = candidate


                country = None

                if len(record) > 4:

                    country = record[4]

                layout = self.detect_track_layout(
                    record
                )
                
                

                if layout == LayoutType.TRACK_STANDARD:

                    age_group, club, result = (
                        self.parse_track_standard(
                            record
                        )
                    )

                elif layout == LayoutType.TRACK_NOTES:

                    age_group, club, result = (
                        self.parse_track_notes(
                            record
                        )
                    )

                elif layout == LayoutType.TRACK_COMPACT_NO_BIRTHYEAR:

                    (
                        birth_year,
                        country,
                        age_group,
                        club,
                        result
                    ) = self.parse_track_compact_no_birthyear(
                        record
                    )

                elif layout == LayoutType.TRACK_COMPACT_NOTES:

                    (
                        country,
                        age_group,
                        club,
                        result
                    ) = self.parse_track_compact_notes(
                        record
                    )

                elif layout == LayoutType.TRACK_AGEGROUP_DETAILS:

                    

                    (
                        age_group,
                        club,
                        result
                    ) = self.parse_track_agegroup_details(
                        record
                    )

                elif layout == LayoutType.TRACK_STEEPLECHASE:

                    (
                        birth_year,
                        country,
                        age_group,
                        club,
                        result
                    ) = self.parse_track_steeplechase(
                        record
                    )

                elif layout == LayoutType.TRACK_NOTES_AGEGROUP:

                    age_group, club, result = (
                        self.parse_track_notes_agegroup(
                            record
                        )
                    )

                else:

                    print(
                        f"UNKNOWN TRACK LAYOUT: {record}"
                    )

                    unhandled_records += 1

                    continue

                if result:

                    result = result.replace("á", "")
                    result = " ".join(result.split())
                    result = re.sub(r"\s+[Qq]$", "", result)

                

                if result and result.endswith("w"):
                    result = result.strip("w")

                
                name = record[1]

                

                name = name.replace("\xa0", " ")

                if "·" in name:
                    name = name.split("·")[0].strip()

                name = re.sub(
                    r"\b[TF]\d{2}(?:,\s*[TF]\d{2})*\b",
                    "",
                    name
                ).strip()

                name = name.title()

                if re.match(r'^\d+\s+', name):

                    print(
                        "\n================="
                    )

                    print(
                        f"SUSPECT NAME: {name}"
                    )

                    print(
                        f"FULL RECORD: {record}"
                    )

                    print(
                        f"EVENT: {record}"
                    )

                    print(
                        "=================\n"
                    )

                if result in ["DNS", "DQ", "NM", "DNF"]:
                    status = result

                if not result and not status:

                    print("\n==============================")
                    print("UNHANDLED TRACK RECORD")
                    print("==============================")
                    print(f"LAYOUT: {layout}")
                    print(f"NAME: {record[1]}")
                    print(f"RECORD LENGTH: {len(record)}")

                    for i, value in enumerate(record):
                        print(f"{i}: {repr(value)}")

                    print("==============================\n")

                        
                   
                athlete = {

                    "place": place,
                    "lane": lane,
                    "name": name,
                    "birth_year": birth_year,
                    "country": country,
                    "age_group": age_group,
                    "club": club,
                    "result": result,
                    "status": status,
                    "source_record": record

                }

            


                athletes.append(athlete)

            except Exception:

                print("\nFAILED RECORD")
                print(record)

                print(
                    f"TYPE(record): {type(record)}"
                )

                raise

        

        return athletes

            

        



    

    def is_field_record_start(self, row):

        if re.match(
            r"^\d+\t\d+$",
            row
        ):
            return True

        if row == "-":
            return True

        # NM example:
        # 1
        # Phillip SMYTH

        if row.isdigit():

            number = int(row)

            if number < 100:
                return True

        return False


    

    def is_track_record_start(self, row):

       
        if re.match(
            r"^\d+\t\d+$",
            row
        ):
            return True

        if row.isdigit():

            number = int(row)

            if number < 100:
                return True

            

        return False






    def is_record_start(self, value):

        if re.match(
            r"^\d+\t\d+$",
            value
        ):
            return True

        if value == "-":
            return True

        if re.match(
            r"^\d+$",
            value
        ):
            return True

        return False





