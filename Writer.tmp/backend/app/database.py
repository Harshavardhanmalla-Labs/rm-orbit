from __future__ import annotations

import os
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()
engine = None
SessionLocal = None
RESOLVED_DATABASE_URL = ""


def _default_database_url() -> str:
    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{data_dir / 'writer.db'}"


def resolve_database_url(database_url: Optional[str] = None) -> str:
    return database_url or os.getenv("WRITER_DATABASE_URL") or _default_database_url()


def setup_database(database_url: Optional[str] = None) -> str:
    global engine, SessionLocal
    global RESOLVED_DATABASE_URL

    resolved_url = resolve_database_url(database_url)
    RESOLVED_DATABASE_URL = resolved_url
    connect_args = {"check_same_thread": False} if resolved_url.startswith("sqlite") else {}

    engine = create_engine(resolved_url, future=True, connect_args=connect_args)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return resolved_url


def init_db() -> None:
    if engine is None:
        setup_database()
    init_mode = os.getenv("WRITER_DB_INIT_MODE", "").strip().lower()
    if not init_mode:
        init_mode = "create_all" if str(engine.url).startswith("sqlite") else "skip"

    if init_mode == "create_all":
        Base.metadata.create_all(bind=engine)
        return

    if init_mode == "skip":
        return

    raise ValueError("Invalid WRITER_DB_INIT_MODE value. Use 'create_all' or 'skip'.")


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        setup_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
