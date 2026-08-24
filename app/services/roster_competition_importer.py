from playwright.sync_api import sync_playwright
from pprint import pprint
import time
import re
import json 




class RosterCompetitionImporter:

    def __init__(
        self,
        competition_url
    ):

        
        self.competition_url = (
            competition_url
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

                try:

                    page.get_by_text(
                        "Accept",
                        exact=True
                    ).click()

                    print("Accepted cookies")

                    page.wait_for_timeout(1000)

                except Exception as e:

                    print(e)


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

            failed_records = 0

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

                print(
                    f"URL after event click: {page.url}"
                )

                page.wait_for_timeout(2000)

                event_data = self.extract_event(
                    page
                )

                print(
                    f"event_type={event_data['event_type']}"
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

                    print(e)

                    athletes = []

                    failed_records += len(
                        event_data["rows"]
                    )

                event_data["athletes"] = athletes
                event_data.pop("rows", None)
                all_events.append(event_data)

                print(
                    f"After parsing event URL: {page.url}"
                )

                

                switch_button = page.get_by_role(
                    "button",
                    name="Switch"
                )

                print(
                   f"Switch count after event: {switch_button.count()}"
                )

                if switch_button.count() > 0:

                    switch_button.first.click()

                    page.wait_for_timeout(1000)

                print(
                    f"After navigation URL: {page.url}"
                )

                      

            athlete_count = sum(
                len(event["athletes"])
                for event in all_events
            )

            missing_results = sum(
                1
                for event in all_events
                for athlete in event["athletes"]
                if not athlete.get("result")
            )

            print("\n===================")
            print("IMPORT SUMMARY")
            print("===================")

            print(
                f"Events: {len(all_events)}"
            )

            print(
                f"Athletes: {athlete_count}"
            )

            print(
                f"Failed records: {failed_records}"
            )

            print(
                f"Missing results: {missing_results}"
            )

            #
            # Show which records are missing results
            #
            for event in all_events:

                for athlete in event["athletes"]:

                    if not athlete.get("result"):

                        print(
                            f"MISSING RESULT | "
                            f"{event['event_name']} | "
                            f"{athlete['name']}"
                        )

            print("===================\n")

            browser.close()

            return all_events



             





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


            event_type = "track"

            #if "\tORDER\t" in text:
            #    event_type = "field"

        except ValueError:

            event_name = None
            event_details = None

        return {
            "event_name": event_name,
            "event_details": event_details,
            "wind": self.extract_wind(text),
            "event_type": event_type,
            "rows": self.extract_rows(text)
        }





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

            parts = record[0].split("\t")

            if len(parts) == 2:
                place = parts[0]
                order = parts[1]
            else:
                place = record[0]

            age_group = None
            club = None
            result = None

            details_parts = record[5].split("\t")

            if len(details_parts) == 2:

                club = details_parts[0]
                result = details_parts[1]

            elif len(details_parts) >= 3:

                club = details_parts[-2]
                result = details_parts[-1]


            for record in records:

                if len(record) < 6:

                    print(
                        f"SHORT FIELD RECORD: {record}"
                    )
                    continue

                status = None

                if len(record) > 7:
                    status = record[7]

            if result in ["NM", "DNS", "DQ"]:
                status = result

            athlete = {

                "place": place,

                "order": order,

                "name": record[1],

                "birth_year": record[2],

                "country": record[4],

                "age_group": age_group,

                "club": club,

                "result": result,

                "status": status

            }

            athletes.append(athlete)

        

        return athletes




    def parse_track_rows(self, rows):
        print(
            "ENTERED parse_track_rows()"
        )

        current_record = []

        records = []

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

        print(
            f"Records found: {len(records)}"
        )

        for r in records:
            print(r)

        print(
            f"Record count: {len(records)}"
        )

        for idx, record in enumerate(records):

            print(
                f"\nRECORD {idx}"
            )

            print(record)

        athletes = []

        for record in records:

            place = None
            lane = None

            parts = record[0].split("\t")

            if len(parts) == 2:
                place = parts[0]
                lane = parts[1]
            else:
                place = record[0]

            age_group = None
            club = None
            result = None
            status = None

            #
            # NORMAL TRACK FORMAT
            #
            if len(record) >= 6:

                birth_year = record[2]

                country = record[4]

                details_index = 5

                #
                # Hurdles format has
                # separate age-group field
                #
                if len(record) > 5:

                    if record[5].startswith("Notes:"):
                        details_index = 6
                    else:
                        details_index = 5

                details_parts = record[details_index].split("\t")

                if len(details_parts) == 1:

                    result = details_parts[0]

                elif len(details_parts) == 2:

                    club = details_parts[0]
                    result = details_parts[1]

                elif len(details_parts) >= 3:

                    club = details_parts[-2]
                    result = details_parts[-1]

                marker = None

                if len(record) > details_index + 1:

                    marker = record[details_index + 1]

                    if marker in ["DNS", "DQ", "NM"]:
                        status = marker
            #
            # COMPACT TRACK FORMAT
            #
            elif len(record) == 4:

                birth_year = None

                country = record[2]

                details_parts = record[3].split("\t")

                if len(details_parts) >= 3:

                    age_group = details_parts[0]
                    club = details_parts[1]
                    result = details_parts[2]

            #
            # UNKNOWN FORMAT
            #
            else:

                print(
                    f"UNHANDLED TRACK RECORD: {record}"
                )

                continue

            if result in ["DNS", "DQ", "NM"]:
                status = result

            if result and result.endswith("w"):
                result = result.strip("w")

            print("\nRECORD")
            print(record)

            print(
                f"name={record[1]}"
            )

            print(
                f"result={result}"
            )

            print(
                f"status={status}"
            )

            print(
                f"club={club}"
            )    
            name = record[1]

            name = name.replace("\xa0", " ")

            if "·" in name:
                name = name.split("·")[0].strip()


            athlete = {

                "place": place,

                "lane": lane,

                "name": name,

                "birth_year": birth_year,

                "country": country,

                "age_group": age_group,

                "club": club,

                "result": result,

                "status": status

            }

            athletes.append(athlete)

        

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





