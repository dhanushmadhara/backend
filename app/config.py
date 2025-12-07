from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Postgres DB URL, e.g. postgresql://user:pass@host:5432/dbname
    database_url: str

    # tesseract / poppler optional overrides
    tesseract_cmd: str | None = None
    poppler_path: str | None = None

    # upload / ocr settings
    upload_dir: str = "/tmp/uploads"
    ocr_lang: str = "eng"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
