from db_services import DBService
from models import Products, VATRates
from sqlalchemy import select, func, or_
import csv
import json

vat_rates = {"Electronics": 20, "Clothing": 14, "Art": 7.9}


class ProductProgram(DBService):

    def __init__(self, db_type: str):
        super().__init__(db_type=db_type)
        self.params = None

    def program_initialise(self):
        self.initialise_db()
        self.load_vat_data()

    def load_vat_data(self):
        vat_rates_list = vat_rates.items()
        self.insert_to_vat(vat_rates_list)
        return

    def load_data(self):
        self.params = self.params[0]
        with (open(f'./{self.params}', mode='r') as f):
            csv_file = csv.DictReader(f)
            for line in csv_file:
                line["Price"] = float(line["Price"])
                line["Quantity"] = int(line["Quantity"])
                values = [line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]]
                del line["Name"], line["Category"], line["Type"], line["Price"], line["Quantity"]
                values.append(json.dumps(line))
                self.insert_to_products(values)
        print(f"Successfully loaded the following data to {self.db_type} : {values}")
        return

    def fetch_item_properties(self) -> set[str]:
        rows = self.table_query(select(Products))
        if not rows:
            return None
        item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in self.params]

        property_1, property_2 = self.table_query(
            select(Products.Extra_attributes).where((Products.id == item_pos_1) | (Products.id == item_pos_2))
        )
        item_set_1 = set(json.loads(property_1).keys())
        item_set_2 = set(json.loads(property_2).keys())
        diff_key_set = item_set_1 - item_set_2
        diff_key_set.update(item_set_2 - item_set_1)
        return diff_key_set

    def take_user_input(self, input_cmd: str):
        cmd, *self.params = input_cmd.split(' ')
        match cmd:
            case "display":
                print([self.row_to_dict(x) for x in self.table_query(select(Products))])
                print([self.row_to_dict(x) for x in self.table_query(select(VATRates))])
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
        adjusted_item = dict(item)
        rate_query = self.table_query(select(VATRates.rate).where(VATRates.Category == item["Category"]))
        rate_val = 0 if not rate_query else rate_query[0]
        percent_increase = 1 + rate_val / 100
        adjusted_item["Price"] *= percent_increase
        return adjusted_item

    def full_text_search(self) -> list[tuple[str, int | str | float]]:
        rows = self.table_query(select(Products))
        if not rows:
            return None

        search_term = f'%{self.params[0]}%'

        items = self.table_query(select(Products).where(or_(
            Products.Category.ilike(search_term),
            Products.Name.ilike(search_term),
            Products.Type.ilike(search_term),
            Products.Extra_attributes.ilike(search_term),
            Products.Price.ilike(search_term),
            Products.Quantity.ilike(search_term)
        )))
        items_data = [self.row_to_dict(x) for x in items]
        return items_data

    def row_to_dict(self, row):
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}

    def item_list_length(self) -> int:
        count = self.table_query(select(func.count()).select_from(Products))
        return int(count[0])

    def show_item_details(self) -> tuple[str, int | str | float]:
        rows = self.table_query(select(Products))
        if not rows:
            return None
        item = self.table_query(select(Products).where(Products.id == int(self.params[0].strip())))
        item_data = [self.row_to_dict(x) for x in item]
        return item_data

    def find_lower_price_min(self) -> list[tuple[str, int | str | float]]:
        rows = self.table_query(select(Products))
        if not rows:
            return None
        min_subquery = select(func.min(Products.Price)).scalar_subquery()
        item = self.table_query(select(Products).where(Products.Price == min_subquery))
        item_data = [self.row_to_dict(x) for x in item]
        return item_data

    def find_highest_price_max(self) -> list[tuple[str, int | str | float]]:
        rows = self.table_query(select(Products))
        if not rows:
            return None
        max_subquery = select(func.max(Products.Price)).scalar_subquery()
        item = self.table_query(select(Products).where(Products.Price == max_subquery))
        item_data = [self.row_to_dict(x) for x in item]
        return item_data

    def find_items_in_category(self) -> list[tuple[str, int | str | float]]:
        rows = self.table_query(select(Products))
        if not rows:
            return None
        items = self.table_query(select(Products).where(Products.Category.ilike(self.params[0])))
        items_data = [self.row_to_dict(x) for x in items]
        return items_data


if __name__ == '__main__':
    while True:
        user_input_db = input('Which database would you like to use? (sqlite, postgres) :')
        if user_input_db == 'sqlite' or user_input_db == 'postgres':
            break
        else:
            continue

    products_program = ProductProgram(user_input_db)
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
