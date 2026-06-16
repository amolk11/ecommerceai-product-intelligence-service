from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(
    log_name="database",
    log_folder="system",
)


@lru_cache(maxsize=1)
def _create_engine() -> Engine:
    """
    Create and cache the SQLAlchemy engine.
    """

    if not settings.db_url:
        logger.error("DB_URL is not configured")
        raise RuntimeError(
            "DB_URL is required for database access"
        )

    logger.info("Creating database engine")

    engine = create_engine(
        settings.db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
    )

    logger.info("Database engine created successfully")

    return engine


def get_engine() -> Engine:
    """
    Return the cached SQLAlchemy engine.
    """
    return _create_engine()


@lru_cache(maxsize=1)
def _create_session_factory() -> sessionmaker:
    """
    Create and cache the session factory.
    """

    logger.info("Creating session factory")

    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.

    Example:

        db: Session = Depends(get_session)
    """

    session_factory = _create_session_factory()

    session = session_factory()

    try:
        yield session

    except Exception:
        logger.exception(
            "Database session failed"
        )
        session.rollback()
        raise

    finally:
        session.close()
        