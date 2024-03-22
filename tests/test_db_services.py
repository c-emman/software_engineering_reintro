from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from software_engineering_reintro.src.db_services import DBService
from software_engineering_reintro.src.models import Base
import pytest


@pytest.fixture(scope="module")
def mock_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def dbsession(mock_engine):
    SessionLocal = sessionmaker(autoflush=False, bind=mock_engine)
    session = SessionLocal()
    yield session
    session.close()


class TestDBService:

    def test_some_database_operation(self, dbsession):
        db_service = DBService(db_type='sqlite', session=dbsession)
