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
            dict_of_new_row[fieldnames[i]] = list_of_new_row[i]
        temp.writerow(dict_of_new_row)


def edit_question(filename, id_num, title, message, fieldnames):
    file = get_all_csv_data(filename)
    if title is not None:
        file[id_num - 1]["title"] = title
    if message is not None:
        file[id_num - 1]["message"] = message
    with open(filename, "w") as newfile:
        newfile = csv.DictWriter(newfile, fieldnames=fieldnames)
        headers = {}
        for i in fieldnames:
            headers[i] = i
        newfile.writerow(headers)
        for i in file:
            newfile.writerow(i)


def delete_question():
    pass


HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
edit_question('sample_data/question_test.csv', 1, "asd3", "asd2", HEADER_DATA)
