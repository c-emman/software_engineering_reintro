shirt = {"Name": "Nike", "Category": "Clothing", "Quantity": 15}

laptop = {"Category": "Electronics", "Price": 1569.99,}

book = {"Name": "Harry Potter", "Price": 6.50, "Quantity": 9}

products = [shirt, laptop, book]


def fetch_item_properties(user_input):
    item_index_list = [int(x) for x in user_input.split(',')]
    item_keys_1 = set(products[int(item_index_list[0])-1].keys())
    item_keys_2 = set(products[int(item_index_list[1])-1].keys())
    diff_key_set = item_keys_1.difference(item_keys_2)
    diff_key_set.update(item_keys_2.difference(item_keys_1))
    return diff_key_set


if __name__ == '__main__':
    userInput = input("Please enter the two items you would like to compare (Comma separated): ")
    properties_diff = fetch_item_properties(userInput)
    print(properties_diff)
