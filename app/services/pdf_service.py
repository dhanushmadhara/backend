from pdf2image import convert_from_bytes

def pdf_bytes_to_images(pdf_bytes: bytes, poppler_path=None):
    kw = {}
    if poppler_path:
        kw["poppler_path"] = poppler_path
    return convert_from_bytes(pdf_bytes, **kw)
