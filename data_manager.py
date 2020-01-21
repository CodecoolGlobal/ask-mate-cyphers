import os
import connection
import time

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
    counter = 0.01
    for question in questions:
        if isinstance(question.get(order_by), int):
            order_dict[question.get(order_by) + counter] = question
            counter += 0.01
        else:
            order_dict[question.get(order_by) + str(counter)] = question
            counter += 0.01
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


def get_all_answers():
    answers = connection.get_all_csv_data(DATA_FILE_PATH_ANSWERS)
    return answers


def get_row_for_id(id_num, file):
    return connection.get_data_for_id(id_num, file)


def get_view_num(id_num):
    connection.numbers_up(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "view_number")


def add_question(file):
    connection.create_question(DATA_FILE_PATH_QUESTIONS, HEADER_DATA, file)


def edit_question(file, id_num):
    title, message = file
    connection.edit_question(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, title, message)


def get_time(table):
    for item in table:
        item['submission_time'] = time.ctime(item.get('submission_time'))
    return table