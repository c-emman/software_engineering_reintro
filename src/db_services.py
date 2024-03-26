from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from models import Base, Products, VATRates, settings


class DBService:
    def __init__(self, db_type: str, session=None):
        self.db_type = db_type
        if session is not None:
            self.session = session
        else:
            if db_type != 'sqlite':
                db_user = settings.POSTGRESQL_USERNAME
                db_pass = settings.POSTGRESQL_PASSWORD
                db_port = settings.POSTGRESQL_PORT
                db_host = settings.POSTGRESQL_HOST
                db_database = settings.POSTGRESQL_DATABASE
                url_obj = URL.create(drivername=db_type, username=db_user, password=db_pass, port=db_port, host=db_host,
                                     database=db_database)
            else:
                url_obj = settings.SQLITE_DATABASE

            self.engine = create_engine(url_obj)
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
                category=item[0],
                rate=item[1]
            )
            try:
                self.session.merge(rate)
                self.session.commit()
            except Exception as e:
                print(e)

    def insert_to_products(self, products_values: list[str | float | int]):

        insert_values = Products(
            name=products_values[0],
            category=products_values[1],
            type=products_values[2],
            price=products_values[3],
            quantity=products_values[4],
            extra_attributes=products_values[5]
        )
        self.session.merge(insert_values)
        self.session.commit()

    def table_query(self, stmt):
        return self.session.scalars(stmt).all()