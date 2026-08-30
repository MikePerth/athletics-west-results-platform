from pathlib import Path
from tempfile import NamedTemporaryFile

from pdfminer.high_level import extract_text

from app.services.meet_manager_pdf_parser import (
    MeetManagerPdfParser
)


class MeetManagerPdfImportService:

    def __init__(self):

        self.parser = (
            MeetManagerPdfParser()
        )

    async def import_pdf(
        self,
        pdf_file
    ):

        with NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                await pdf_file.read()
            )

            pdf_path = temp_file.name

        text = extract_text(
            Path(pdf_path)
        )

        events = self.parser.parse(
            text
        )

        return events