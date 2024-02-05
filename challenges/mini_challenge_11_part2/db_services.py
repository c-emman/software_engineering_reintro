from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from models import Base, Products, VATRates
from dotenv import load_dotenv
import os


class DBService:
    def __init__(self, db_type: str):
        self.db_type = db_type
        load_dotenv()
        db_user = os.getenv(f'{db_type.upper()}_USERNAME')
        db_pass = os.getenv(f'{db_type.upper()}_PASSWORD')
        db_port = os.getenv(f'{db_type.upper()}_PORT')
        db_host = os.getenv(f'{db_type.upper()}_HOST')
        db_database = os.getenv(f'{db_type.upper()}_DATABASE')
        url_obj = URL.create(drivername=db_type, username=db_user, password=db_pass, port=db_port, host=db_host,
                             database=db_database) if db_type != 'sqlite' else "sqlite:///db/products.db"
        self.engine = create_engine(url_obj, echo=True)
        self.session = None

    def initialise_db(self):
        try:
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            self.session = Session(bind=self.engine)
        except Exception as e:
            print(e)

    def insert_to_vat(self, vat_values: list[tuple[str, float]]):
        for item in vat_values:
            rate = VATRates(
                Category=item[0],
                rate=item[1]
            )
            try:
                self.session.merge(rate)
                self.session.commit()
            except Exception as e:
                print(e)

    def insert_to_products(self, products_values: list[str | float | int]):

        insert_values = Products(
            Name=products_values[0],
            Category=products_values[1],
            Type=products_values[2],
            Price=products_values[3],
            Quantity=products_values[4],
            Extra_attributes=products_values[5]
        )
        self.session.merge(insert_values)
        self.session.commit()

    def table_query(self, stmt):
        return self.session.scalars(stmt).all()
