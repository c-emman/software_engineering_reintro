shirt = {"Name": "Nike", "Category": "Clothing", "Quantity": 15}

laptop = {"Category": "Electronics", "Price": 1569.99, }

book = {"Name": "Harry Potter", "Price": 6.50, "Quantity": 9}

products = [shirt, laptop, book]


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


def item_list_length():
    list_length = len(products)
    return list_length


def show_item_details(input_cmd):
    index = int(input_cmd.strip("show "))-1
    return products[index]


if __name__ == '__main__':
    userInput = input("Please enter the command you would like to do: ")
    result = take_user_input(userInput)
    print(result)
