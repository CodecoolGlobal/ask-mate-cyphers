import csv


# filename: 'sample_data/question.csv', 'sample_data/answer.csv'
def get_all_user_story(filename):
    with open(filename, 'r') as cs_file:
        csv_read = csv.DictReader(cs_file)
        table = []
        for line in csv_read:
            table.append(dict(line))
    return table
