import re
from .base_parser import BaseParser

class PatientDetailsParser(BaseParser):
    def parse(self):
        return {
            "patient_name": self.get_patient_name(),
            "phone_number": self.get_phone_number(),
            "medical_problems": self.get_medical_problems(),
            "hepatitis_b_vaccination": self.get_hepb_status()
        }

    def get_patient_name(self):
        m = re.search(r"(Name|Patient Information)[:\s]+([A-Za-z .,-]+)", self.text)
        return m.group(2).strip() if m else None

    def get_phone_number(self):
        m = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", self.text)
        return m.group(0) if m else None

    def get_hepb_status(self):
        m = re.search(r"Hepatitis B.*?(Yes|No)", self.text, flags=re.DOTALL|re.IGNORECASE)
        return m.group(1) if m else None

    def get_medical_problems(self):
        m = re.search(r"Medical Problems[:\s]+(.*)", self.text, flags=re.IGNORECASE)
        return m.group(1).strip() if m else None
