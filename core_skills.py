import random
# rand_list =
rand_list = [random.randint(1, 19) for _ in range(20)]
print(rand_list)

# list_comprehension_below_10 =
list_comprehension_below_10 = [i for i in rand_list if i < 10]
print(list_comprehension_below_10)

# list_comprehension_below_10 =
list_comprehension_below_10 = list(filter(lambda x: x<10, rand_list))
print(list_comprehension_below_10)