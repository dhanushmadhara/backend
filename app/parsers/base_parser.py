from abc import ABC, abstractmethod
import re

class BaseParser(ABC):
    def __init__(self, text: str):
        self.text = text or ""

    @abstractmethod
    def parse(self) -> dict:
        pass

    def find_first(self, patterns, flags=0):
        for p in patterns:
            m = re.search(p, self.text, flags)
            if m:
                return m
        return None
