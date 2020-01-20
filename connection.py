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


def create_question(filename, fieldnames, dict_of_new_row):
    with open(filename, 'a') as file:
        file = csv.DictWriter(file, fieldnames=fieldnames)
        file.writerow(dict_of_new_row)


def edit_question():
    pass


def delete_question():
    pass
