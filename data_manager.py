import os
import connection

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answer.csv'
HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']


def get_headers():
    headers = []
    for header in HEADER_DATA:
        capitalized_header = ''
        header_list = list(header.split('_'))
        for word in header_list:
            capitalized_header += word.capitalize()
            capitalized_header += ' '
        headers.append(capitalized_header.rstrip())
    return headers


def get_all_questions():
    questions = connection.get_all_csv_data(DATA_FILE_PATH_QUESTIONS)
    return questions

