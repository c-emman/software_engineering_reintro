shirt = {"Name": "Nike", "Category": "Clothing", "Price": 49.99, "Quantity": 15}

laptop = {"Name": "Lenovo", "Category": "Electronics", "Price": 1569.99, "Quantity": 6}

book = {"Name": "Harry Potter", "Category": "Fiction", "Price": 6.50, "Quantity": 9}

products = [shirt, laptop, book]


def display_item():
    not_exists = True
    while not_exists:
        item_number = int(input("Please enter item position number: "))
        if item_number in range(len(products)):
            return products[item_number]
        else:
            print("""
            The value you entered has no position. 
            Please enter an integer in the required range
            """)


if __name__ == "__main__":
    item = display_item()
    print(item)
