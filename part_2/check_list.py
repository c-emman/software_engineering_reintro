
list_1 = ["banana", "apple", "pear", "orange"]

test_fruit = ["apple"]

set1 = set(list_1)

set2 = set(test_fruit)

does_fruit_exist = len( set1 & set2) > 0

if __name__ == "__main__":
    print(f"{test_fruit} is present in list: {does_fruit_exist} ")