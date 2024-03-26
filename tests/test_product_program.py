import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.product_program import ProductProgram
from src.db_services import DBService
from src.models import Base, Products, VATRates
import pytest
import tempfile
import csv
import os


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
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()
    session.close()


@pytest.fixture
def test_products_data():
    return [["Test Product 1", "electronics", "gadget", 19.99, 10, '{"color": "blue", "weight": "60g"}'],
            ["Test Product 2 full text", "clothing", "shirt", 42.50, 7, '{"brand": "Hugo Boss", "size": "XXL"}'],
            ["Test Product 3", "fiction", "book", 11.99, 29, '{"author": "J.K Rowling", "sequels": 7}'],
            ["Test Product 4", "art", "art full text", 1233.00, 2, '{"author": "Banksy", "age": "21 years"}']]


class TestProductsProgram:

    def test_load_data(self, dbsession):
        with tempfile.TemporaryDirectory() as tmpdirname:
            data_dir = os.path.join(tmpdirname, "data")
            os.makedirs(data_dir)

            csv_path = os.path.join(data_dir, "test_data.csv")
            with open(csv_path, "w", newline="") as csvfile:
                fieldnames = ["name", "category", "type", "price", "quantity", "color", "weight"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({"name": "Test Product", "category": "electronics",
                                 "type": "gadget", "price": 19.99, "quantity": 10,
                                 "color": "blue", "weight": "120g"})

            products_program = ProductProgram(db_type='sqlite', session=dbsession)
            products_program.params = ["test_data.csv"]
            os.chdir(tmpdirname)
            products_program.load_data()
            result = dbsession.execute(select(Products.name, Products.category,
                                              Products.type, Products.price,
                                              Products.quantity, Products.extra_attributes)).first()

            result_list = list(result)
            cleaned_attributes = json.loads(result_list[-1])
            final_result = set(result_list[:5] + list(cleaned_attributes.values()))
            assert {"Test Product", "electronics", "gadget", 19.99, 10, "blue", "120g"} == final_result

    def test_fetch_item_properties(self, dbsession, test_products_data):
        products_program = ProductProgram(db_type='sqlite', session=dbsession)
        for item in test_products_data:
            products_program.insert_to_products(item)

        products_program.params = '1,2'
        diff_props = products_program.fetch_item_properties()

        assert {"brand", "size", "color", "weight"} == diff_props

    def test_full_text_search(self, dbsession, test_products_data):
        products_program = ProductProgram(db_type='sqlite', session=dbsession)
        for item in test_products_data:
            products_program.insert_to_products(item)

        products_program.params = ['full text']

        result = products_program.full_text_search()

        final_result = {value for d in result for value in d.values()}

        assert {"Test Product 2 full text", "clothing", "shirt", 42.50, 7, '{"brand": "Hugo Boss", "size": "XXL"}',
                "Test Product 4", "art", "art full text", 1233.00, 2, 4,
                '{"author": "Banksy", "age": "21 years"}'} == final_result
