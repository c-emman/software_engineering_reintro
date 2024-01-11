import sqlite3
from sqlite3 import Error


class ProductsDB:

    def __init__(self, db_file):
        self.conn = None
        self.db_file = db_file
        self.cur = None

    def create_connection(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return

    def create_cursor(self) -> None:
        if self.conn is not None:
            try:
                self.cur = self.conn.cursor()
                print("Successfully connected and created cursor")
            except Error as e:
                print(e)
        return

    def define_schema(self) -> None:
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS products (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            Name text not NULL,
                            Category text not NULL,
                            Type text,
                            Price real,
                            Quantity integer not NULL, 
                            Extra_attributes text);
                            """)
            self.cur.execute("""CREATE TABLE IF NOT EXISTS vat_rates (
                            Category text PRIMARY KEY,
                            rate real );
                            """)

        except Error as e:
            print(e)
        return

    def insert_values_to_rates_table(self, values: list):
        try:
            self.cur.executemany(f"INSERT into vat_rates VALUES (?,?)", values)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_values_to_products_table(self, values: list):
        try:
            self.cur.execute(f"""INSERT into products VALUES 
            (:id, :Name, :Category, :Type, :Price, :Quantity, :Extra_attributes)""", values)
            self.conn.commit()
        except Error as e:
            print(e)

    def sql_query(self, query: str):
        try:
            res = self.cur.execute(f"{query}")
            rows = res.fetchall()
            return rows
        except Error as e:
            print(e)
            return None

    def select_all(self):
        try:
            res = self.cur.execute("SELECT * from products")
            rows = res.fetchall()
            return rows
        except Error as e:
            print(e)
            return None
