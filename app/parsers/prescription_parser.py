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
        # FIXED invalid dash placement (escaped)
        m = re.search(r"Name[:\s]+([A-Za-z .,\-]+)", self.text)
        return m.group(1).strip() if m else None

    def get_address(self):
        m = re.search(
            r"Address[:\s]+(.+?)(?:\n\n|\nDirections|$)", 
            self.text, 
            flags=re.DOTALL
        )
        return m.group(1).strip() if m else None

    def get_medicines(self):
        # First pattern for block extraction
        m = re.search(
            r"Address[\s\S]*?\n(.*?)\nDirections",
            self.text, 
            flags=re.IGNORECASE | re.DOTALL
        )
        if m:
            return "\n".join(
                [ln.strip() for ln in m.group(1).split("\n") if ln.strip()]
            )

        # FIXED dash inside character class
        meds = re.findall(
            r'^[A-Z][A-Za-z0-9 \-]+ \d+\s?mg.*$',
            self.text,
            flags=re.MULTILINE
        )
        return "\n".join(meds) if meds else None

    def get_directions(self):
        m = re.search(
            r"Directions[:\s]+(.+?)Refill",
            self.text,
            flags=re.IGNORECASE | re.DOTALL
        )
        return m.group(1).strip() if m else None

    def get_refills(self):
        m = re.search(
            r"Refill[:\s]+(\d+)",
            self.text,
            flags=re.IGNORECASE
        )
        return int(m.group(1)) if m else None
