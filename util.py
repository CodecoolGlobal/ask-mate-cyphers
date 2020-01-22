def find_row_index_by_id(table, id_num):
    for index in range(len(table)):
        if table[index]["id"] == id_num:
            return index


def get_data_for_id(id_num, file):
    for row in file:
        if row['id'] == id_num:
            return row
