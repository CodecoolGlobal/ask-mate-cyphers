import csv


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
    with open(filename, 'a') as file:
        temp = csv.DictWriter(file, fieldnames=fieldnames)
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


def write_file(fieldnames, file, filename):
    with open(filename, "w") as newfile:
        newfile = csv.DictWriter(newfile, fieldnames=fieldnames)
        headers = {}
        for i in fieldnames:
            headers[i] = i
        newfile.writerow(headers)
        for i in file:
            newfile.writerow(i)
