import os
import connection

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answer.csv'
HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
DEFAULT_ORDER_BY = 'id'
DEFAULT_ORDER_DIR = 'desc'

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


def get_all_questions(order_by=DEFAULT_ORDER_BY, order_direction=DEFAULT_ORDER_DIR):
    if order_direction == 'desc':
        order_direction = True
    elif order_direction == 'asc':
        order_direction = False
    questions = connection.get_all_csv_data(DATA_FILE_PATH_QUESTIONS)
    for i in range(len(questions)):
        for k, v in questions[i].items():
            try:
                questions[i][k] = int(v)
            except ValueError:
                pass
    order_dict = {}
    for question in questions:
        order_dict[question.get(order_by)] = question
    sorted_dict = sorted(order_dict.items(), reverse=order_direction)
    questions = []
    for item in sorted_dict:
        questions.append(item[1])
    return questions


def get_new_order_dir(order_direction):
    if order_direction == 'asc':
        return 'desc'
    elif order_direction == 'desc':
        return 'asc'
