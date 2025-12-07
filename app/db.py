from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Use asyncpg driver
DATABASE_URL = settings.database_url
# Make sure DATABASE_URL begins with "postgresql+asyncpg://"
if DATABASE_URL.startswith("postgresql://"):
    # adapt legacy scheme if necessary
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
