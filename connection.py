import csv
import time
import util


# CRUD: create, read, update, delete
# filename: 'sample_data/question.csv', 'sample_data/answer.csv'
def get_all_csv_data(filename):  # read
    with open(filename, 'r') as cs_file:
        csv_read = csv.DictReader(cs_file)
        table = []
        for line in csv_read:
            table.append(dict(line))
    return table


def create_row(filename, fieldnames, list_of_new_row, q_id_num=None):
    file = get_all_csv_data(filename)
    if q_id_num is None:
        add_list = [0, 0, int(time.time()), int(file[-1]["id"]) + 1]
    else:
        add_list = [q_id_num, 0, int(time.time()), int(file[-1]["id"]) + 1]
    for i in add_list:
        list_of_new_row.insert(0, i)
    with open(filename, 'a') as newfile:
        temp = csv.DictWriter(newfile, fieldnames=fieldnames)
        dict_of_new_row = {}
        for i in range(len(list_of_new_row)):
            dict_of_new_row.update({fieldnames[i]: list_of_new_row[i]})
        temp.writerow(dict_of_new_row)


def edit_row(filename, id_num, fieldnames, title=None, message=None):
    file = get_all_csv_data(filename)
    index = util.find_row_index_by_id(file, id_num)
    if title is not None:
        file[index]["title"] = title
    if message is not None:
        file[index]["message"] = message
    file[index]["submission_time"] = int(time.time())
    write_file(fieldnames, file, filename)


def delete_row_by_id(filename, id_num, fieldnames):
    file = get_all_csv_data(filename)
    del_index = 0
    for i in range(len(file)):
        if file[i]["id"] == str(id_num):
            del_index = i
    del file[del_index]
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


def numbers_modify(filename, id_num, fieldnames, column, value):
    file = get_all_csv_data(filename)
    index = util.find_row_index_by_id(file, id_num)
    file[index][column] = int(file[index][column]) + value
    write_file(fieldnames, file, filename)


def delete_answers(filename, fieldnames, id_num=None, question_id=None):
    if id_num is not None:
        delete_row_by_id(filename, id_num, fieldnames)
    elif question_id is not None:
        file = get_all_csv_data(filename)
        list_of_id = []
        for line in file:
            if int(line["question_id"]) == question_id:
                list_of_id.append(int(line["id"]))
        for i in list_of_id:
            delete_row_by_id(filename, i, fieldnames)
