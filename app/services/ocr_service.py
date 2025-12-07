import pytesseract
from PIL import Image
from typing import List
from ..utils.image_utils import preprocess_image
from ..config import settings

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

def ocr_image(image: Image.Image, lang: str | None = None) -> str:
    lang = lang or settings.ocr_lang
    processed = preprocess_image(image)
    return pytesseract.image_to_string(processed, lang=lang)

def ocr_images(images: List[Image.Image]) -> str:
    texts = []
    for i, img in enumerate(images):
        t = ocr_image(img)
        texts.append(f"\n--- PAGE {i+1} ---\n{t}")
    return "\n".join(texts)

