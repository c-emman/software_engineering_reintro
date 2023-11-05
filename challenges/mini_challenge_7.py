shirt = {"Name": "Nike", "Category": "Clothing", "Price": 32.50, "Quantity": 15, "Size": "XL", "Colour": "Red"}

laptop = {"Name": "Nike", "Category": "Electronics", "Price": 1569.99, "Quantity": 6, "Weight": "150g", "OS": "Windows"}

book = {"Name": "Harry Potter", "Category": "Fiction", "Price": 6.50, "Quantity": 9, "Author": "J.K Rowling",
        "Cover type": "Hardcover"}

products = [shirt, laptop, book]


def fetch_item_properties(user_input):
    item_index_list = [int(x) for x in user_input.split(',')]
    item_keys_1 = set(products[int(item_index_list[0]) - 1].keys())
    item_keys_2 = set(products[int(item_index_list[1]) - 1].keys())
    diff_key_set = item_keys_1.difference(item_keys_2)
    diff_key_set.update(item_keys_2.difference(item_keys_1))
    return diff_key_set


def take_user_input(input_cmd):
    if input_cmd == "len":
        list_length = item_list_length()
        return list_length
    if input_cmd == "show 2":
        item_details = show_item_details()
        return item_details
    if input_cmd == "cmp 1, 3":
        diff_key_set = fetch_item_properties("1, 3")
        return diff_key_set
    if input_cmd == "pmin":
        lowest_price_item = find_lower_price_item()
        return lowest_price_item
    if input_cmd == "pmax":
        highest_price_item = find_highest_price_item()
        return highest_price_item
    if "cat" in input_cmd:
        category_name = input_cmd[3:].strip()
        item_list_category = find_items_in_category(category_name)
        return item_list_category


def item_list_length():
    list_length = len(products)
    return list_length


def show_item_details():
    return products[2]


def find_lower_price_item():
    lower_price = products[0]["Price"]
    lower_product = products[0]
    for item in products:
        if lower_price > item["Price"]:
            lower_price = item["Price"]
            lower_product = item
    return lower_product


def find_highest_price_item():
    higher_price = products[0]["Price"]
    higher_product = products[0]
    for item in products:
        if higher_price < item["Price"]:
            higher_price = item["Price"]
            higher_product = item
    return higher_product


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
