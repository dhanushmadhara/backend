from pdf2image import convert_from_bytes
from typing import List
from PIL import Image
from ..config import settings

def pdf_bytes_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    kwargs = {}
    if settings.poppler_path:
        kwargs["poppler_path"] = settings.poppler_path
    return convert_from_bytes(pdf_bytes, **kwargs)
