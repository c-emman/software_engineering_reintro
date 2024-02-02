from products_db import ProductsDB
import csv
import json

vat_rates = {"Electronics": 20, "Clothing": 14, "Art": 7.9}


class ProductProgram(ProductsDB):

    def __init__(self, db_file: str, db_type: str):
        super().__init__(db_file=db_file, db_type=db_type)
        self.params = None

    def program_initialise(self):
        self.create_connection()
        self.create_cursor()
        self.define_schema()
        self.load_vat_data()

    def load_vat_data(self):
        vat_rates_list = vat_rates.items()
        self.insert_values_to_rates_table(vat_rates_list)
        return

    def load_data(self):
        self.params = self.params[0]
        with (open(f'./{self.params}', mode='r') as f):
            csv_file = csv.DictReader(f)
            for line in csv_file:
                line["Price"] = float(line["Price"])
                line["Quantity"] = int(line["Quantity"])
                values = [None, line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]] \
                    if self.db_type == 'sqlite' \
                    else [line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]]
                del line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]
                values.append(json.dumps(line))
                self.insert_values_to_products_table(values)
                # self.insert_values_to_search_table(values[1:])
        print(f"Successfully loaded the following data to {self.db_type} : {values[1:]}")
        return

    def fetch_item_properties(self) -> set[str]:
        rows = self.sql_query("SELECT * from products")
        if not rows:
            return None
        item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in self.params]
        property_1, property_2 = self.sql_query(f"""SELECT Extra_attributes from products 
                where id={item_pos_1} OR id={item_pos_2};""")
        item_set_1 = set(json.loads(property_1[0]).keys())
        item_set_2 = set(json.loads(property_2[0]).keys())
        diff_key_set = item_set_1 - item_set_2
        diff_key_set.update(item_set_2 - item_set_1)
        return diff_key_set

    def take_user_input(self, input_cmd: str):
        cmd, *self.params = input_cmd.split(' ')
        match cmd:
            case "display":
                print(self.sql_query("SELECT * from products;"))
                return
            case "len":
                list_length = self.item_list_length()
                return list_length
            case "show":
                item_details = self.show_item_details()
                return item_details
            case "cmp":
                diff_key_set = self.fetch_item_properties()
                return diff_key_set
            case "pmin":
                lowest_price_item = self.find_lower_price_min()
                return lowest_price_item
            case "pmax":
                highest_price_item = self.find_highest_price_max()
                return highest_price_item
            case "cat":
                item_list_category = self.find_items_in_category()
                return item_list_category
            case "search":
                search_items = self.full_text_search()
                return search_items
            case "load":
                self.load_data()

    def format_item(self, item) -> dict[str, int | str | float]:
        product_keys = ['id', 'Name', 'Category', 'Type', 'Price', 'Quantity', 'Extra_attributes']
        paired_item = zip(product_keys, item)
        adjusted_item = dict(paired_item)
        adjusted_item["Price"] = adjusted_item["Price"] if self.db_type == 'sqlite' else \
            float(adjusted_item["Price"].removeprefix('£').replace(',', ''))
        rate_query = self.sql_query(f"SELECT rate from vat_rates where Category='{item[2]}';")
        rate_val = 0 if len(rate_query) == 0 else rate_query[0][0]
        percent_increase = 1 + rate_val / 100
        adjusted_item["Price"] *= percent_increase
        return adjusted_item

    def full_text_search(self) -> list[tuple[str, int | str | float]]:
        rows = self.sql_query("SELECT * from products;")
        if not rows:
            return None

        if self.db_type == 'sqlite':
            search_term = self.params[0]
            items = self.sql_query(f"""SELECT * from products WHERE 
                                    Name LIKE '%{search_term}%' OR 
                                    Category LIKE '%{search_term}%' OR 
                                    Type LIKE '%{search_term}%'OR 
                                    Price LIKE '%{search_term}%' OR 
                                    Quantity LIKE '%{search_term}%' OR 
                                    Extra_attributes LIKE '%{search_term}%' ;""")
            return items

        elif self.db_type == 'postgres':
            search_term = f'%{self.params[0]}%'
            items = self.sql_query_params("""SELECT * FROM products WHERE Name LIKE %s 
                                                OR Category LIKE %s 
                                                OR Type LIKE %s 
                                                OR Price::text LIKE %s 
                                                OR Quantity::text LIKE %s 
                                                OR Extra_attributes LIKE %s""", [search_term]*6)

            return items

    def item_list_length(self) -> int:
        count = self.sql_query("SELECT COUNT(id) from products;")
        return int(count[0][0])

    def show_item_details(self) -> tuple[str, int | str | float]:
        rows = self.sql_query("SELECT * from products;")
        if not rows:
            return None
        item = self.sql_query(f"SELECT * from products WHERE id={int(self.params[0].strip())};")
        return item

    def find_lower_price_min(self) -> list[tuple[str, int | str | float]]:
        rows = self.sql_query("SELECT * from products;")
        if not rows:
            return None
        items = self.sql_query("SELECT * from products WHERE Price=(SELECT MIN(Price) from products);")
        return items

    def find_highest_price_max(self) -> list[tuple[str, int | str | float]]:
        rows = self.sql_query("SELECT * from products;")
        if not rows:
            return None
        items = self.sql_query("SELECT * from products WHERE Price=(SELECT MAX(Price) from products);")
        return items

    def find_items_in_category(self) -> list[tuple[str, int | str | float]]:
        rows = self.sql_query("SELECT * from products;")
        if not rows:
            return None
        items = self.sql_query(f"SELECT * from products WHERE Category LIKE '{self.params[0]}';")
        return items


if __name__ == '__main__':
    while True:
        user_input_db = input('Which database would you like to use? (sqlite, postgres) :')
        if user_input_db == 'sqlite' or user_input_db == 'postgres':
            break
        else:
            continue

    products_program = ProductProgram('./db/products.db', user_input_db)
    products_program.program_initialise()

    while True:
        user_input = input("Please enter the command you would like to do: ")
        if user_input == "quit":
            break

        result = products_program.take_user_input(user_input)

        if type(result) is list:
            print([products_program.format_item(item) for item in result])
        elif result is None:
            pass
        else:
            print(result)
