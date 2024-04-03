from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.product_webapp import app
from src.product_program import ProductProgram
from src.models import Base
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
    # for table in reversed(Base.metadata.sorted_tables):
    #     session.execute(table.delete())
    # session.commit()
    # session.close()
    session.close()


@pytest.fixture(scope="function")
def test_app(dbsession):
    # Create a ProductProgram instance using the test session
    test_product_app = ProductProgram(db_type='sqlite', session=dbsession)
    test_product_app.program_initialise()

    # Use middleware to manually set the application state for testing
    @app.middleware("http")
    async def override_db_session_middleware(request: Request, call_next):
        request.state.db = test_product_app
        response = await call_next(request)
        return response

    yield app

    # Cleanup: Remove the middleware after the test to avoid side effects
    app.user_middleware.pop()


@pytest.fixture(scope="function")
def client(test_app):
    with TestClient(test_app) as client:
        yield client


def test_some_endpoint(client):
    response = client.post('/products/load',
                           json={'file_str': 'clothing.csv'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Successfully loaded product data'}
