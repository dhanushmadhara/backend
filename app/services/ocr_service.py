import pytesseract
from PIL import Image
from ..utils.image_utils import preprocess_image
from ..config import settings

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

def ocr_image(image: Image.Image, lang="eng"):
    processed = preprocess_image(image)
    return pytesseract.image_to_string(processed, lang=lang)

def ocr_images(images):
    results = []
    for idx, img in enumerate(images):
        text = ocr_image(img, settings.ocr_lang)
        results.append(f"\n--- PAGE {idx+1} ---\n{text}")
    return "\n".join(results)
