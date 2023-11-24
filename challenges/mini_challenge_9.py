shirt = {"Name": "Nike", "Category": "Clothing", "Price": 32.50, "Quantity": 15, "Size": "XL", "Colour": "Red"}

laptop = {"Name": "Nike", "Category": "Electronics", "Price": 1569.99, "Quantity": 6, "Weight": "150g", "OS": "Windows"}

book = {"Name": "Harry Potter", "Category": "Fiction", "Price": 6.50, "Quantity": 9, "Author": "J.K Rowling",
        "Cover type": "Hardcover"}
artwork = {"Name": "Jumbotron Art", "Category": "Art", "Price": 5400, "Quantity": 3, "Author": "K.F Parkins",
           "Age": "29 years"}

products = [shirt, laptop, book, artwork]

vat_rates = {"Electronics": 20, "Clothing": 14}


def fetch_item_properties(user_input):
    number_vals = user_input.strip("cmp ")
    item_pos_1, item_pos_2 = [int(x) for x in number_vals.split(',')]
    item_keys_1 = set(products[item_pos_1 - 1].keys())
    item_keys_2 = set(products[item_pos_2 - 1].keys())
    diff_key_set = item_keys_1.difference(item_keys_2)
    diff_key_set.update(item_keys_2.difference(item_keys_1))
    return diff_key_set


def take_user_input(input_cmd):
    if input_cmd == "len":
        list_length = item_list_length()
        return list_length
    if "show" in input_cmd:
        item_details = show_item_details(input_cmd)
        return item_details
    if "cmp" in input_cmd:
        diff_key_set = fetch_item_properties(input_cmd)
        return diff_key_set
    if input_cmd == "pmin":
        lowest_price_item = find_lower_price_min()
        return lowest_price_item
    if input_cmd == "pmax":
        highest_price_item = find_highest_price_max()
        return highest_price_item
    if "cat" in input_cmd:
        category_name = input_cmd[3:].strip()
        item_list_category = find_items_in_category(category_name)
        return item_list_category
    if "search" in input_cmd:
        items = full_text_search(input_cmd)
        return items


def full_text_search(input_cmd):
    search_term = input_cmd.strip("search ")
    items = [item for item in products if (search_term in item["Name"]) or (search_term in item["Category"])]
    return items


def item_list_length():
    list_length = len(products)
    return list_length


def show_item_details(input_cmd):
    index = int(input_cmd.strip("show ")) - 1
    return products[index]


def find_lower_price_min():
    item = min(products, key=lambda product: product["Price"])
    return item


def find_highest_price_max():
    item = max(products, key=lambda product: product["Price"])
    return item


def find_items_in_category(category):
    item_list = [x for x in products if x["Category"] == category]
    return item_list


if __name__ == '__main__':
    while True:
        userInput = input("Please enter the command you would like to do: ")
        if userInput == "quit":
            break
        result = take_user_input(userInput)
        print(result)