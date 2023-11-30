shirt = {"Name": "Nike", "Category": "Clothing", "Quantity": 15}

laptop = {"Category": "Electronics", "Price": 1569.99,}

book = {"Name": "Harry Potter", "Price": 6.50, "Quantity": 9}

products = [shirt, laptop, book]


def fetch_item_properties(params):
    item_pos_1, item_pos_2 = [int(x.replace(',', '')) for x in params]
    item_keys_1 = set(products[item_pos_1 - 1].keys())
    item_keys_2 = set(products[item_pos_2 - 1].keys())
    diff_key_set = item_keys_1.difference(item_keys_2)
    diff_key_set.update(item_keys_2.difference(item_keys_1))
    return diff_key_set


if __name__ == '__main__':
    user_input = input("Please enter the two items you would like to compare (Comma separated): ")
    print(fetch_item_properties(user_input))
