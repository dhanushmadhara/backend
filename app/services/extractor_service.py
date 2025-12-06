from ..services.pdf_service import pdf_bytes_to_images
from ..services.ocr_service import ocr_images
from ..parsers.patient_parser import PatientDetailsParser
from ..parsers.prescription_parser import PrescriptionParser
from ..config import settings

def extract_from_pdf_bytes(pdf_bytes: bytes, file_format: str) -> dict:
    images = pdf_bytes_to_images(pdf_bytes, settings.poppler_path)
    text = ocr_images(images)
    if file_format == "patient_details":
        return PatientDetailsParser(text).parse()
    if file_format == "prescription":
        return PrescriptionParser(text).parse()
    raise ValueError("Invalid document format")
