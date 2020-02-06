def get_new_order_dir(order_direction):
    if order_direction == 'asc':
        return 'desc'
    else:
        return 'asc'


def modify_search(search):
    length = 0
    char = ["'", "%"]
    while length != len(search):
        print(length, end="")
        print(len(search))
        if search[length] in char:
            search = search[:length] + "\\" + search[length:]
            length += 2
        else:
            length += 1
    return search
