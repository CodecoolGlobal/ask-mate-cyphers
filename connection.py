import csv
import time


# CRUD: create, read, update, delete
# filename: 'sample_data/question.csv', 'sample_data/answer.csv'
def get_all_csv_data(filename):  # read
    with open(filename, 'r') as cs_file:
        csv_read = csv.DictReader(cs_file)
        table = []
        for line in csv_read:
            table.append(dict(line))
    return table


def create_question(filename, fieldnames, list_of_new_row):
    file = get_all_csv_data(filename)
    add_list = [0, 0, int(time.time()), int(file[-1]["id"]) + 1]
    for i in add_list:
        list_of_new_row.insert(0, i)
    print(list_of_new_row)
    with open(filename, 'a') as newfile:
        temp = csv.DictWriter(newfile, fieldnames=fieldnames)
        dict_of_new_row = {}
        for i in range(len(list_of_new_row)):
            dict_of_new_row.update({fieldnames[i]: list_of_new_row[i]})
        temp.writerow(dict_of_new_row)


def edit_question(filename, id_num, fieldnames, title=None, message=None):
    file = get_all_csv_data(filename)
    if title is not None:
        file[id_num - 1]["title"] = title
    if message is not None:
        file[id_num - 1]["message"] = message
    file[id_num - 1]["submission_time"] = int(time.time())
    write_file(fieldnames, file, filename)


def delete_question(filename, id_num, fieldnames):
    file = get_all_csv_data(filename)
    del_index = 0
    for i in range(len(file)):
        if file[i]["id"] == str(id_num):
            del_index = i
    del file[del_index]
    for i in range(del_index, len(file)):
        file[i]["id"] = int(file[i]["id"]) - 1
    write_file(fieldnames, file, filename)


def write_file(fieldnames, save_file, filename):
    with open(filename, "w") as newfile:
        newfile = csv.DictWriter(newfile, fieldnames=fieldnames)
        headers = {}
        for i in fieldnames:
            headers[i] = i
        newfile.writerow(headers)
        for i in save_file:
            newfile.writerow(i)


def numbers_up(filename, id_num, fieldnames, column):
    file = get_all_csv_data(filename)
    file[id_num - 1][column] = int(file[id_num - 1][column]) + 1
    write_file(fieldnames, file, filename)


def get_data_for_id(id_num, file):
    for row in file:
        if row['id'] == id_num:
            return row
