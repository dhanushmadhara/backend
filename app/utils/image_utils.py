import cv2
import numpy as np
from PIL import Image

def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    img = np.array(pil_img.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    scale = 1.5 if max(h, w) < 2000 else 1.0
    if scale != 1.0:
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 61, 11)
    return processed

