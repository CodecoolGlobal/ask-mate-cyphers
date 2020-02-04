def get_new_order_dir(order_direction):
    if order_direction == 'asc':
        return 'desc'
    else:
        return 'asc'