# import os
import connection
# import time
# import util
#
# DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/question.csv'
# DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answer.csv'
# HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
# HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
# DEFAULT_ORDER_BY = 'id'
# DEFAULT_ORDER_DIR = 'desc'


def get_all_questions_with_limit(order_by, desc):
    query = '''
    SELECT *
    FROM question
    ORDER BY {} {} LIMIT 5'''.format(order_by, desc)
    return connection.db_mod_with_return(query=query)


def get_all_questions_without_limit(order_by, desc):
    query = '''
        SELECT *
        FROM question
        ORDER BY {} {} '''.format(order_by, desc)
    return connection.db_mod_with_return(query=query)


def get_all_answers():
    query = '''
    SELECT *
    FROM answer
    ORDER BY id'''
    return connection.db_mod_with_return(query=query)


def get_question(id_num):
    query = '''
    SELECT *
    FROM question
    WHERE id={}'''.format(id_num)
    return connection.db_mod_with_return(query=query)


def vote(table, id_num, num, column):
    query = '''
    UPDATE {}
    SET {} = {} + {}
    WHERE id={}'''.format(table, column, column, num, id_num)
    connection.db_mod_without_return(query=query)
#
#
# def add_question(file):
#     connection.create_row(DATA_FILE_PATH_QUESTIONS, HEADER_DATA, file)
#
#
# def add_answer(file, id_num):
#     connection.create_row(DATA_FILE_PATH_ANSWERS, HEADER_ANSWERS, file, id_num)
#
#
# def edit_question(file, id_num):
#     try:
#         title, message, image = file
#     except ValueError:
#         image = None
#         title = file[0]
#         message = file[1]
#     connection.edit_row(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, title, message, image)
#
#
# def vote_up(id_num):
#     connection.numbers_modify(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "vote_number", 1)
#
#
# def vote_down(id_num):
#     connection.numbers_modify(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA, "vote_number", -1)
#
#
# def delete_question(id_num):
#     connection.delete_row_by_id(DATA_FILE_PATH_QUESTIONS, id_num, HEADER_DATA)
#     connection.delete_answers(DATA_FILE_PATH_ANSWERS, HEADER_ANSWERS, id_num)
#
#
# def delete_answer(id_num):
#     connection.delete_row_by_id(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS)
#
#
# def answer_vote_up(id_num):
#     connection.numbers_modify(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, "vote_number", 1)
#
#
# def answer_vote_down(id_num):
#     connection.numbers_modify(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, "vote_number", -1)
#
#
# def edit_answer(file, id_num):
#     try:
#         message, image = file
#     except ValueError:
#         message = file[0]
#         image = None
#     connection.edit_row(DATA_FILE_PATH_ANSWERS, id_num, HEADER_ANSWERS, message=message, image=image)
