# test_pdf.py

from pdfminer.high_level import extract_text

pdf_file = r"C:\Users\MichaelHolmes\Downloads\AthleticsWestRecordsPlatform\country_records.pdf"

text = extract_text(pdf_file)

print(text[:10000])