import bcrypt


def get_new_order_dir(order_direction):
    if order_direction == 'asc':
        return 'desc'
    else:
        return 'asc'


def modify_search(search):
    length = 0
    char = ["'", "%"]
    while length != len(search):
        if search[length] in char:
            search = search[:length] + "\\" + search[length:]
            length += 2
        else:
            length += 1
    return search


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
