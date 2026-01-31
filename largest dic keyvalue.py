my_dict = {'a': 10, 'b': 20, 'c': 15}
max_key = min(my_dict, key=my_dict.get)
print("Key with the largest value:", max_key)
