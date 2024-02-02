import sqlite3
import psycopg2
from sqlite3 import Error


class ProductsDB:

    def __init__(self, db_file, db_type):
        self.conn = None
        self.db_file = db_file
        self.cur = None
        self.db_type = db_type

    def create_connection(self) -> None:
        match self.db_type.lower():
            case 'sqlite':
                try:
                    self.conn = sqlite3.connect(self.db_file)
                    print(sqlite3.version)
                except Error as e:
                    print(e)
                return
            case 'postgres':
                try:
                    self.conn = psycopg2.connect(dbname='productsdb',
                                                 user='chrisemmanuel',
                                                 password='password',
                                                 port='5432')
                    connected = 'Connected to postgres database' if self.conn.closed == 0 else 'Not connected to postgres'
                    print(connected)
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)
                return

    def create_cursor(self) -> None:
        if self.conn is not None:
            try:
                self.cur = self.conn.cursor()
                print("Successfully connected and created cursor")
            except (Exception, psycopg2.DatabaseError, Error) as e:
                print(e)
        return

    def define_schema(self) -> None:
        match self.db_type:
            case 'sqlite':
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
            case 'postgres':
                try:
                    self.cur.execute("""CREATE TABLE IF NOT EXISTS products (
                                        id SERIAL PRIMARY KEY,
                                        Name varchar(200) not NULL,
                                        Category varchar(200) not NULL,
                                        Type varchar(200),
                                        Price money,
                                        Quantity integer not NULL, 
                                        Extra_attributes varchar(500));
                                        """)
                    self.cur.execute("""CREATE TABLE IF NOT EXISTS vat_rates (
                                        Category varchar(200) PRIMARY KEY,
                                        rate float8);
                                        """)
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)
                return

    def insert_values_to_rates_table(self, values: list):
        match self.db_type:
            case 'sqlite':
                try:
                    self.cur.executemany(f"INSERT or IGNORE into vat_rates VALUES (?,?)", values)
                    self.conn.commit()
                except Error as e:
                    print(e)
            case 'postgres':
                try:
                    self.cur.executemany(f"INSERT INTO vat_rates VALUES (%s, %s) ON CONFLICT DO NOTHING", values)
                    self.conn.commit()
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)

    def insert_values_to_products_table(self, values: list):
        match self.db_type:
            case 'sqlite':
                try:
                    self.cur.execute(f"""INSERT into products VALUES 
                    (:id, :Name, :Category, :Type, :Price, :Quantity, :Extra_attributes)""", values)
                    self.conn.commit()
                except Error as e:
                    print(e)
            case 'postgres':
                try:
                    self.cur.execute(f"""INSERT INTO products (name, category, type, price, quantity, extra_attributes) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", values)
                    self.conn.commit()
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)

    def sql_query(self, query: str):
        match self.db_type:
            case 'sqlite':
                try:
                    res = self.cur.execute(f"{query}")
                    rows = res.fetchall()
                    return rows
                except Error as e:
                    print(e)
                    return None
            case 'postgres':
                try:
                    self.cur.execute(f"{query}")
                    rows = self.cur.fetchall()
                    return rows
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)
                    return None

    def sql_query_params(self, query: str, values: list):
        match self.db_type:
            case 'sqlite':
                try:
                    res = self.cur.execute(f"{query}", values)
                    rows = res.fetchall()
                    return rows
                except Error as e:
                    print(e)
                    return None
            case 'postgres':
                try:
                    self.cur.execute(f"{query}", values)
                    rows = self.cur.fetchall()
                    return rows
                except (Exception, psycopg2.DatabaseError) as e:
                    print(e)
                return None

    def close_connection(self):
        self.cur.close()
        self.conn.close()
