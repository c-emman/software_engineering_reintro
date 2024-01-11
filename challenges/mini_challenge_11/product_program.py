import csv
import json

from products_db import ProductsDB

products = list()

vat_rates = {"Electronics": 20, "Clothing": 14, "Art": 7.9}


class ProductProgram(ProductsDB):

    def __init__(self, db_file):
        super().__init__(db_file=db_file)
        self.params = None

    def progam_initialise(self):
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
        with open(f'./{self.params}', mode='r') as f:
            csv_file = csv.DictReader(f)
            for line in csv_file:
                line["Price"] = float(line["Price"])
                line["Quantity"] = int(line["Quantity"])
                values = [None, line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]]
                del line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]
                values.append(json.dumps(line))
                print(values)
                self.insert_values_to_products_table(values)

    def fetch_item_properties(self) -> set[str]:
        rows = self.sql_query("SELECT * from products")
        if not rows:
            return None
        item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in self.params]
        property_1, property_2 = self.sql_query(f"""SELECT Extra_attributes from products 
                where id={item_pos_1} OR id={item_pos_2}""")
        item_set_1 = set(json.loads(property_1[0]).keys())
        item_set_2 = set(json.loads(property_2[0]).keys())
        diff_key_set = item_set_1 - item_set_2
        diff_key_set.update(item_set_2 - item_set_1)
        return diff_key_set

    def take_user_input(self, input_cmd: str):
        cmd, *self.params = input_cmd.split(' ')
        match cmd:
            case "display":
                return self.select_all()
            case "len":
                list_length = self.item_list_length()
                return list_length
            case "show":
                item_details = self.show_item_details(self.params)
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
                # print(products)

    def format_item(self, item):
        adjusted_item = dict(item)
        rate_query = self.sql_query(f"SELECT rate from vat_rates where Category={item['Category']}")
        rate_val = rate_query[0][0] if not None else 0
        percent_increase = 1 + rate_val/100
        adjusted_item["Price"] *= percent_increase
        return adjusted_item

    def full_text_search(self) -> list[dict[str, int | str | float]]:
        if not products:
            return None
        search_term = self.params[0]
        items = [item for item in products if
                 (search_term.lower() in item["Name"].lower()) or (search_term.lower() in item["Category"].lower())]
        return items

    def item_list_length(self) -> int:
        return len(products)

    def show_item_details(self) -> dict[str, int | str | float]:
        if not products:
            return None
        index = int(self.params[0].strip()) - 1
        return products[index]

    def find_lower_price_min(self) -> dict[str, int | str | float]:
        if not products:
            return None
        item = min(products, key=lambda product: product["Price"])
        return item

    def find_highest_price_max(self) -> dict[str, int | str | float]:
        if not products:
            return None
        item = max(products, key=lambda product: product["Price"])
        return item

    def find_items_in_category(self) -> list[dict[str, int | str | float]]:
        if not products:
            return None
        item_list = [x for x in products if x["Category"].lower() == self.params[0].lower()]
        return item_list


if __name__ == '__main__':

    products_program = ProductProgram('./db/products.db')
    products_program.progam_initialise()
    while True:
        user_input = input("Please enter the command you would like to do: ")
        if user_input == "quit":
            break
        result = products_program.take_user_input(user_input)
        # if type(result) is dict:
        #     print(format_item(result))
        # elif type(result) is list:
        #     print([format_item(item) for item in result])
        # else:
        print(result)
