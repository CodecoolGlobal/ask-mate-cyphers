import os
import connection
import time
import util

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answer.csv'
HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
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


def get_all_answers():
    answers = connection.get_all_csv_data(DATA_FILE_PATH_ANSWERS)
    return answers


def get_new_order_dir(order_direction):
    if order_direction == 'asc':
        return 'desc'
    elif order_direction == 'desc':
        return 'asc'


def get_all_answers():
    answers = connection.get_all_csv_data(DATA_FILE_PATH_ANSWERS)
    return answers


def get_row_for_id(id_num, file):
    return util.get_data_for_id(id_num, file)


def get_view_num(id_num):
    connection.numbers_modify(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "view_number", 1)


def add_question(file):
    connection.create_row(DATA_FILE_PATH_QUESTIONS, HEADER_DATA, file)


def add_answer(file, id_num):
    connection.create_row(DATA_FILE_PATH_ANSWERS, HEADER_ANSWERS, file, id_num)


def edit_question(file, id_num):
    try:
        title, message, image = file
    except ValueError:
        image = None
        title = file[0]
        message = file[1]
    connection.edit_row(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, title, message, image)


def get_time(table):
    for item in table:
        item['submission_time'] = time.ctime(item.get('submission_time'))
    return table


def vote_up(id_num):
    connection.numbers_modify(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "vote_number", 1)


def vote_down(id_num):
    connection.numbers_modify(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "vote_number", -1)


def delete_question(id_num):
    connection.delete_row_by_id(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA)
    connection.delete_answers(DATA_FILE_PATH_ANSWERS, HEADER_ANSWERS, question_id=id_num)


def delete_answer(id_num):
    connection.delete_row_by_id(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS)


def answer_vote_up(id_num):
    connection.numbers_modify(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, "vote_number", 1)


def answer_vote_down(id_num):
    connection.numbers_modify(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, "vote_number", -1)


def edit_answer(file, id_num):
    try:
        message, image = file
    except ValueError:
        message = file[0]
        image = None
    connection.edit_row(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, message=message, image=image)
