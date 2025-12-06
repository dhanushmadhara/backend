from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .services.extractor_service import extract_from_pdf_bytes

app = FastAPI(title="Medical PDF Extractor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/extract")
async def extract_route(file_format: str = Form(...), file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    result = extract_from_pdf_bytes(pdf_bytes, file_format)
    return result
