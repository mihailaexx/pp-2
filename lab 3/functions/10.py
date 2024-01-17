def make_unique(list):
    new_list = []
    for x in list:
        if list.count(x) == 1:
            new_list.append(x)
    return new_list
print(*make_unique([1, 1, 2, 3]))