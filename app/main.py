import json
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .db import AsyncSessionLocal, engine
from .models import Base as ModelsBase
from .services.extractor_service import extract_from_pdf_bytes
from .crud import create_record, search_records
from .config import settings
import asyncio

app = FastAPI(title="Medical PDF Extractor API")

# CORS - set appropriate origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables at startup
@app.on_event("startup")
async def on_startup():
    # create tables (run sync create_all using run_sync)
    async with engine.begin() as conn:
        await conn.run_sync(ModelsBase.metadata.create_all)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/v1/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/extract")
async def extract_endpoint(file_format: str = Form(...), file: UploadFile = File(...),
                           db: AsyncSession = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    pdf_bytes = await file.read()
    try:
        extracted = extract_from_pdf_bytes(pdf_bytes, file_format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    patient_name = extracted.get("patient_name") or extracted.get("patient", {}).get("name")
    raw_text = extracted.pop("_raw_text", None) or ""
    # persist
    rec = await create_record(db, file_format=file_format, patient_name=patient_name,
                              raw_text=raw_text, extracted=extracted)
    # return record id and extracted data
    return {"id": rec.id, "extracted": extracted}

@app.get("/v1/search")
async def search(q: str | None = None, page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    results = await search_records(db, q=q, page=page, limit=limit)
    return {"items": results, "page": page, "limit": limit}
