from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.db_services import DBService
from src.models import Base, Products, VATRates
import pytest
import json


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


@pytest.fixture
def load_vat_data():
    # Load test data
    return [('fiction', 32.1), ('clothing', 9), ('electronics', 0.23)]


@pytest.fixture
def load_products_data():
    extra_attributes = {'size': 'L', 'colour': 'Red', 'rating': 5 / 10}
    return ['Nike Air Jordan t-shirt', 'clothing', 't-shirt', 34.99, 11, json.dumps(extra_attributes)]


class TestDBService:

    def test_vat_insert_operation(self, dbsession, load_vat_data):
        db_service = DBService(db_type='sqlite', session=dbsession)
        db_service.insert_to_vat(load_vat_data)
        values = dbsession.execute(select(VATRates.category, VATRates.rate)).all()
        # Convert the results to a list of tuples if not already
        values_tuples = [(category, rate) for category, rate in values]
        assert values_tuples == load_vat_data

    def test_products_insert(self, dbsession, load_products_data):
        db_service = DBService(db_type='sqlite', session=dbsession)
        db_service.insert_to_products(load_products_data)
        values_test = dbsession.execute(select(Products.name, Products.category,
                                               Products.type, Products.price,
                                               Products.quantity, Products.extra_attributes)).first()

        assert load_products_data == list(values_test)
