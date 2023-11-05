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


def item_list_length():
    list_length = len(products)
    return list_length


def show_item_details():
    return products[2]


if __name__ == '__main__':

    while True:
        userInput = input("Please enter the command you would like to do: ")
        if userInput == "quit":
            break
        result = take_user_input(userInput)
        print(result)
