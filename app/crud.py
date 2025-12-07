from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Record
import json

async def create_record(db: AsyncSession, file_format: str, patient_name: str | None,
                        raw_text: str, extracted: dict):
    rec = Record(
        file_format=file_format,
        patient_name=patient_name,
        raw_text=raw_text,
        extracted_json=json.dumps(extracted)
    )
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return rec

async def search_records(db: AsyncSession, q: str | None = None, page: int = 1, limit: int = 20):
    stmt = select(Record)
    if q:
        stmt = stmt.where(Record.patient_name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Record.created_at.desc()).offset((page-1)*limit).limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    out = []
    for r in rows:
        try:
            data = json.loads(r.extracted_json)
        except Exception:
            data = {}
        out.append({
            "id": r.id,
            "patient_name": r.patient_name,
            "file_format": r.file_format,
            "created_at": r.created_at.isoformat(),
            "data": data
        })
    return out
