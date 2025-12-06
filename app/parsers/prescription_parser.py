import re
from .base_parser import BaseParser

class PrescriptionParser(BaseParser):
    def parse(self):
        return {
            "patient_name": self.get_name(),
            "patient_address": self.get_address(),
            "medicines": self.get_medicines(),
            "directions": self.get_directions(),
            "refills": self.get_refills()
        }

    def get_name(self):
        m = re.search(r"Name[:\s]+([A-Za-z .,-]+)", self.text)
        return m.group(1).strip() if m else None

    def get_address(self):
        m = re.search(r"Address[:\s]+(.+)", self.text)
        return m.group(1).strip() if m else None

    def get_medicines(self):
        m = re.search(r"Address.*?\n(.+?)Directions", self.text, flags=re.DOTALL)
        return m.group(1).strip() if m else None

    def get_directions(self):
        m = re.search(r"Directions[:\s]+(.+?)Refill", self.text, flags=re.DOTALL)
        return m.group(1).strip() if m else None

    def get_refills(self):
        m = re.search(r"Refill[:\s]+(\d+)", self.text)
        return int(m.group(1)) if m else None
