import connection


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


def get_one_answer(id_num):
    query = '''
    SELECT *
    FROM answer
    WHERE id = {}'''.format(id_num)
    return connection.db_mod_with_return(query=query)


def get_comment(id_type, id_num):
    query = '''
    SELECT *
    FROM comment
    WHERE {} = {}'''.format(id_type, id_num)
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


def add_question_comment(message, id_num):
    query = '''
    INSERT INTO comment(question_id, message, submission_time)
    VALUES ({}, '{}', current_timestamp)'''.format(id_num, message)
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


def edit_comment(id_num, message):
    query = '''
    UPDATE comment
    SET  message = '{}'
    WHERE id = {}'''.format(message, id_num)
    return connection.db_mod_without_return(query=query)


def delete(table, id_num):
    query = '''
    DELETE FROM {}
    WHERE id = {}'''.format(table, id_num)
    return connection.db_mod_without_return(query=query)


def delete_by_question_id(table, id_num):
    query = '''
    DELETE FROM {}
    WHERE question_id = {}'''.format(table ,id_num)
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
