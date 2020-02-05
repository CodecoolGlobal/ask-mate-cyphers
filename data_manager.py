import connection
import datetime


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


def get_answers_by_question_id(question_id):
    query = '''
    SELECT *
    FROM answer
    WHERE question_id = {}'''.format(question_id)
    return connection.db_mod_with_return(query=query)


def get_answer(id_num):
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


def get_all_comment():
    query = '''
    SELECT *
    FROM comment'''
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
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image = file
    except ValueError:
        image = None
        title = file[0]
        message = file[1]
    query = '''
    INSERT INTO question(submission_time ,view_number, vote_number, title, message, image)
    VALUES ('{}', 0, 0, '{}', '{}', '{}')'''.format(sub_time, title, message, image)
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


def add_comment(id_type, message, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
    INSERT INTO comment({}, message, submission_time)
    VALUES ({}, '{}', '{}')'''.format(id_type, id_num, message, sub_time)
    connection.db_mod_without_return(query=query)


def edit_question(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image = file
    except ValueError:
        image = None
        title = file[0]
        message = file[1]
    query = '''
        UPDATE question
        SET title = '{}', message = '{}', image = '{}', submission_time = '{}'
        WHERE id = {}'''.format(title, message, image, sub_time, id_num)
    return connection.db_mod_without_return(query=query)


def edit_comment(id_num, message):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
    UPDATE comment
    SET  message = '{}', submission_time = '{}'
    WHERE id = {}'''.format(message, sub_time, id_num)
    return connection.db_mod_without_return(query=query)


def delete_by_id(table, id_type, id_num):
    query = '''
    DELETE FROM {}
    WHERE {} = {}'''.format(table, id_type, id_num)
    return connection.db_mod_without_return(query=query)


def edit_answer(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        message, image = file
    except ValueError:
        message = file[0]
        image = None
    query = '''
        UPDATE answer
        SET message = '{}', image = '{}', submission_time = '{}'
        WHERE id = {}'''.format(message, image, sub_time, id_num)
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
    for tag in old_tags:
        if tag not in new_tags:
            tag_id = get_tag_id(tag)[0]['id']
            query = '''
            DELETE FROM question_tag
            WHERE question_id = '{}' AND tag_id = '{}' '''.format(question_id, tag_id)
            connection.db_mod_without_return(query=query)
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
            connection.db_mod_without_return(query=query)
