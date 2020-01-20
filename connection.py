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


def edit_question():
    pass


def delete_question():
    pass


HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
file = 'sample_data/question.csv'
lista = [1, 2, 3, 4, "asd", "asd2"]
create_question(file, HEADER_DATA, lista)
