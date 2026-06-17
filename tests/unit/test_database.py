import pytest

from app.core import database

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def clear_database_caches():
    database._create_engine.cache_clear()
    database._create_session_factory.cache_clear()
    yield
    database._create_engine.cache_clear()
    database._create_session_factory.cache_clear()


def test_get_engine_creates_and_caches_configured_engine(monkeypatch):
    created = []
    engine = object()

    def fake_create_engine(url, **kwargs):
        created.append((url, kwargs))
        return engine

    monkeypatch.setattr(database.settings, "db_url", "postgresql://test/db")
    monkeypatch.setattr(database, "create_engine", fake_create_engine)

    assert database.get_engine() is engine
    assert database.get_engine() is engine
    assert created == [
        (
            "postgresql://test/db",
            {
                "pool_pre_ping": True,
                "pool_size": 10,
                "max_overflow": 20,
                "pool_recycle": 1800,
            },
        )
    ]


def test_get_engine_raises_when_db_url_is_missing(monkeypatch):
    monkeypatch.setattr(database.settings, "db_url", None)

    with pytest.raises(RuntimeError, match="DB_URL is required"):
        database.get_engine()


def test_create_session_factory_uses_cached_engine(monkeypatch):
    engine = object()
    calls = []

    class FakeSessionMaker:
        def __init__(self, **kwargs):
            calls.append(kwargs)

    monkeypatch.setattr(database, "get_engine", lambda: engine)
    monkeypatch.setattr(database, "sessionmaker", FakeSessionMaker)

    session_factory = database._create_session_factory()

    assert isinstance(session_factory, FakeSessionMaker)
    assert calls == [
        {
            "bind": engine,
            "autoflush": False,
            "autocommit": False,
            "expire_on_commit": False,
        }
    ]


def test_get_session_yields_and_closes_session(monkeypatch):
    session = FakeSession()

    monkeypatch.setattr(database, "_create_session_factory", lambda: lambda: session)

    generator = database.get_session()

    assert next(generator) is session
    with pytest.raises(StopIteration):
        next(generator)
    assert session.closed is True
    assert session.rolled_back is False


def test_get_session_rolls_back_and_closes_on_exception(monkeypatch):
    session = FakeSession()

    monkeypatch.setattr(database, "_create_session_factory", lambda: lambda: session)

    generator = database.get_session()

    assert next(generator) is session
    with pytest.raises(ValueError, match="boom"):
        generator.throw(ValueError("boom"))
    assert session.rolled_back is True
    assert session.closed is True


class FakeSession:
    def __init__(self):
        self.closed = False
        self.rolled_back = False

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True
