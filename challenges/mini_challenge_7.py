shirt = {"Name": "Nike", "Category": "Clothing", "Price": 32.50, "Quantity": 15, "Size": "XL", "Colour": "Red"}

laptop = {"Name": "Nike", "Category": "Electronics", "Price": 1569.99, "Quantity": 6, "Weight": "150g", "OS": "Windows"}

book = {"Name": "Harry Potter", "Category": "Fiction", "Price": 6.50, "Quantity": 9, "Author": "J.K Rowling",
        "Cover type": "Hardcover"}

products = [shirt, laptop, book]


def fetch_item_properties(params):
    item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in params]
    item_keys_1 = set(products[item_pos_1 - 1].keys())
    item_keys_2 = set(products[item_pos_2 - 1].keys())
    diff_key_set = item_keys_1.difference(item_keys_2)
    diff_key_set.update(item_keys_2.difference(item_keys_1))
    return diff_key_set


def take_user_input(input_cmd):
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


def item_list_length():
    return len(products)


def show_item_details(params):
    index = int(params[0].strip()) - 1
    return products[index]


def find_lower_price_min():
    item = min(products, key=lambda product: product["Price"])
    return item


def find_highest_price_max():
    item = max(products, key=lambda product: product["Price"])
    return item


def find_items_in_category(category):
    item_list = [x for x in products if x["Category"] == category[0]]
    return item_list


if __name__ == '__main__':
    while True:
        user_input = input("Please enter the command you would like to do: ")
        if user_input == "quit":
            break
        print(take_user_input(user_input))
