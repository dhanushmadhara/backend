import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    tesseract_cmd: str | None = None
    poppler_path: str | None = None
    upload_dir: str = "/tmp/uploads"
    ocr_lang: str = "eng"
    class Config:
        env_file = ".env"
settings = Settings()
