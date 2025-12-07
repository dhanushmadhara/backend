from ..services.pdf_service import pdf_bytes_to_images
from ..services.ocr_service import ocr_images
from ..parsers.patient_parser import PatientDetailsParser
from ..parsers.prescription_parser import PrescriptionParser
from ..config import settings

def extract_from_pdf_bytes(pdf_bytes: bytes, file_format: str) -> dict:
    images = pdf_bytes_to_images(pdf_bytes)
    if not images:
        raise ValueError("No pages found in PDF")
    text = ocr_images(images)

    if file_format == "prescription":
        parsed = PrescriptionParser(text).parse()
    elif file_format == "patient_details":
        parsed = PatientDetailsParser(text).parse()
    else:
        raise ValueError("Unsupported file_format")

    # attach raw_text so we can store it
    parsed["_raw_text"] = text
    return parsed

