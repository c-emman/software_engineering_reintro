import csv

products = list()

vat_rates = {"Electronics": 20, "Clothing": 14, "Art": 7.9}


def load_data(params):
    with open(f'./{params[0]}', mode='r') as f:
        csv_file = csv.DictReader(f)
        for line in csv_file:
            line["Price"] = float(line["Price"])
            line["Quantity"] = int(line["Quantity"])
            products.append(line)


def fetch_item_properties(params: list[str]) -> set[str]:
    if not products:
        return None
    item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in params]
    item_keys_1 = set(products[item_pos_1 - 1].keys())
    item_keys_2 = set(products[item_pos_2 - 1].keys())
    diff_key_set = item_keys_1 - item_keys_2
    diff_key_set.update(item_keys_2 - item_keys_1)
    return diff_key_set


def take_user_input(input_cmd: str):
    cmd, *params = input_cmd.split(' ')
    match cmd:
        case "len":
            list_length = item_list_length()
            return list_length
        case "show":
            item_details = show_item_details(params)
            return item_details
        case "cmp":
            diff_key_set = fetch_item_properties(params)
            return diff_key_set
        case "pmin":
            lowest_price_item = find_lower_price_min()
            return lowest_price_item
        case "pmax":
            highest_price_item = find_highest_price_max()
            return highest_price_item
        case "cat":
            item_list_category = find_items_in_category(params)
            return item_list_category
        case "search":
            search_items = full_text_search(params)
            return search_items
        case "load":
            load_data(params)
            print(products)


def format_item(item):
    adjusted_item = dict(item)
    percent_increase = 1 + vat_rates.get(item["Category"], 0) / 100
    adjusted_item["Price"] *= percent_increase
    return adjusted_item


def full_text_search(params: list[str]) -> list[dict[str, int | str | float]]:
    if not products:
        return None
    search_term = params[0]
    items = [item for item in products if
             (search_term.lower() in item["Name"].lower()) or (search_term.lower() in item["Category"].lower())]
    return items


def item_list_length() -> int:
    return len(products)


def show_item_details(params: list[str]) -> dict[str, int | str | float]:
    if not products:
        return None
    index = int(params[0].strip()) - 1
    return products[index]


def find_lower_price_min() -> dict[str, int | str | float]:
    if not products:
        return None
    item = min(products, key=lambda product: product["Price"])
    return item


def find_highest_price_max() -> dict[str, int | str | float]:
    if not products:
        return None
    item = max(products, key=lambda product: product["Price"])
    return item


def find_items_in_category(category: list[str]) -> list[dict[str, int | str | float]]:
    if not products:
        return None
    item_list = [x for x in products if x["Category"].lower() == category[0].lower()]
    return item_list


if __name__ == '__main__':
    while True:
        user_input = input("Please enter the command you would like to do: ")
        if user_input == "quit":
            break
        result = take_user_input(user_input)
        if type(result) is dict:
            print(format_item(result))
        elif type(result) is list:
            print([format_item(item) for item in result])
        else:
            print(result)
