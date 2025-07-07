from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Для разработки используем SQLite, в продакшн PostgreSQL
if settings.database_url.startswith("postgresql"):
    engine = create_engine(settings.database_url)
else:
    # SQLite для разработки
    engine = create_engine(
        "sqlite:///./hr_assistant.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()