# import os
import connection
from datetime import datetime
# import util
#
# DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH_QUESTIONS') if 'DATA_FILE_PATH_QUESTIONS' in os.environ else 'sample_data/question.csv'
# DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH_ANSWERS') if 'DATA_FILE_PATH_ANSWERS' in os.environ else 'sample_data/answer.csv'
# HEADER_DATA = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 	'message', 'image']
# HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
# DEFAULT_ORDER_BY = 'id'
# DEFAULT_ORDER_DIR = 'desc'


def get_all_questions_with_limit(order_by='id', desc='DESC'):
    query = '''
    SELECT *
    FROM question
    ORDER BY {} {} LIMIT 5'''.format(order_by, desc)
    return connection.db_mod_with_return(query=query)


def get_all_questions_without_limit(order_by='id', desc='DESC'):
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


def get_answers(question_id):
    query = '''
    SELECT *
    FROM answer
    WHERE question_id = {}'''.format(question_id)
    return connection.db_mod_with_return(query=query)


def get_one_answer(id_num):
    query = '''
    SELECT *
    FROM answer
    WHERE id = {}'''.format(id_num)
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


def add_question(file):
    try:
        title, message, image = file
    except ValueError:
        image = None
        title = file[0]
        message = file[1]
    query = '''
    INSERT INTO question(submission_time ,view_number, vote_number, title, message, image)
    VALUES (current_timestamp , 0, 0, '{}', '{}', '{}')'''.format(title, message, image)
    connection.db_mod_without_return(query=query)


def add_answer(file, id_num):
    try:
        message, image = file
    except ValueError:
        image = None
        message = file[0]
    query = '''
    INSERT INTO answer(submission_time, vote_number, question_id, message, image)
    VALUES (current_timestamp, 0, {}, '{}', '{}')'''.format(id_num, message, image)
    connection.db_mod_without_return(query=query)


def edit_question(file, id_num):
    try:
        title, message, image = file
    except ValueError:
        image = None
        title = file[0]
        message = file[1]
    query = '''
        UPDATE question
        SET title = '{}', message = '{}', image = '{}'
        WHERE id = {}'''.format(title, message, image, id_num)
    return connection.db_mod_without_return(query=query)


def delete(table, id_num):
    query = '''
    DELETE FROM {}
    WHERE id = {}'''.format(table, id_num)
    return connection.db_mod_without_return(query=query)


def delete_answer_by_question_id(id_num):
    query = '''
    DELETE FROM answer
    WHERE question_id = {}'''.format(id_num)
    return connection.db_mod_without_return(query=query)


def edit_answer(file, id_num):
    try:
        message, image = file
    except ValueError:
        message = file[0]
        image = None
    query = '''
        UPDATE answer
        SET message = '{}', image = '{}'
        WHERE id = {}'''.format(message, image, id_num)
    return connection.db_mod_without_return(query=query)


def get_tags(question_id):
    query = '''
        SELECT tag.name
        FROM question_tag
        INNER JOIN tag ON question_tag.tag_id=tag.id
        WHERE question_id = {}'''.format(question_id)
    return connection.db_mod_with_return(query=query)


def get_tag_id(tag_name):
    query = '''
        SELECT id
        FROM tag
        WHERE name = '{}' '''.format(tag_name)
    return connection.db_mod_with_return(query=query)


def get_all_tag_names():
    query = '''
        SELECT name
        FROM tag'''
    return connection.db_mod_with_return(query=query)


def modify_tags(question_id, new_tags):
    old_tags = [tag['name'] for tag in get_tags(question_id)]
    all_tags = [tag['name'] for tag in get_all_tag_names()]
    print(old_tags)
    print(new_tags)
    print(get_tag_id('sql')[0]['id'])
    print([tag['name'] for tag in get_all_tag_names()])
    for tag in old_tags:
        if tag not in new_tags:
            tag_id = get_tag_id(tag)[0]['id']
            query = '''
            DELETE FROM question_tag
            WHERE question_id = '{}' AND tag_id = '{}' '''.format(question_id, tag_id)
            return connection.db_mod_without_return(query=query)
    for tag in new_tags:
        if tag not in old_tags:
            if tag not in all_tags:
                query = '''
                INSERT INTO tag (name)
                VALUES ('{}')'''.format(tag)
                connection.db_mod_without_return(query=query)
            tag_id = get_tag_id(tag)[0]['id']
            query = '''
            INSERT INTO question_tag(question_id, tag_id)
            VALUES ({}, {})'''.format(question_id, tag_id)
            return connection.db_mod_without_return(query=query)
