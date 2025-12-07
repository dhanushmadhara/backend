from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(300), index=True, nullable=True)
    file_format = Column(String(100), index=True, nullable=False)
    raw_text = Column(Text, nullable=True)
    extracted_json = Column(Text, nullable=False)  # store JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
