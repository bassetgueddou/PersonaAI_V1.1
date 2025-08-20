from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
engine = create_engine(settings.database_url or 'postgresql+psycopg2://basset:secret@db:5432/bassetbot', pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
