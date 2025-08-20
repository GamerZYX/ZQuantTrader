from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def init_engine_and_tables() -> None:
    global engine, SessionLocal
    if engine is None:
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        engine = create_engine(settings.database_url, pool_pre_ping=True, pool_recycle=3600, connect_args=connect_args)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        # Deferred import to avoid circulars
        from . import models  # noqa: F401
        Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    global SessionLocal
    if SessionLocal is None:
        init_engine_and_tables()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


