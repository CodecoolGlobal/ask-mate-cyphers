import csv
import os

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/questions.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answers.csv'
HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']


# filename: 'sample_data/question.csv', 'sample_data/answer.csv'
def get_all_user_story(filename):
    with open(filename, 'r') as cs_file:
        csv_read = csv.DictReader(cs_file)
        table = []
        for line in csv_read:
            table.append(dict(line))
    return table
