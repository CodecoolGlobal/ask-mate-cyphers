import connection
import datetime
import util


def get_all_questions_with_limit(order_by='id', desc='DESC'):
    query = '''
    SELECT *
    FROM question
    ORDER BY %s %s LIMIT 5'''
    list_of_var = [order_by, desc]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_questions_without_limit(order_by='id', desc='DESC'):
    query = '''
        SELECT *
        FROM question
        ORDER BY %s %s'''
    list_of_var = [order_by, desc]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_answers_by_question_id(question_id):
    query = '''
    SELECT *
    FROM answer
    WHERE question_id = %s'''
    list_of_var = [question_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_answer(id_num):
    query = '''
    SELECT *
    FROM answer
    WHERE id = %s'''
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_comment(id_type, id_num):
    query = '''
    SELECT *
    FROM comment
    WHERE %s = %s'''
    list_of_var = [id_type, id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_comment():
    query = '''
    SELECT *
    FROM comment'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_question(id_num):
    query = '''
    SELECT *
    FROM question
    WHERE id=%s'''
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def vote(table, id_num, num, column):
    query = '''
    UPDATE %s
    SET %s = %s + %s
    WHERE id=%s'''
    list_of_var = [table, column, column, num, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_question(file):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image = file
        query = '''
            INSERT INTO question(submission_time ,view_number, vote_number, title, message, image)
            VALUES (%s, 0, 0, %s, %s, %s)'''
        list_of_var = [sub_time, title, message, image]
    except ValueError:
        title = file[0]
        message = file[1]
        query = '''
        INSERT INTO question(submission_time ,view_number, vote_number, title, message)
        VALUES (%s, 0, 0, %s, %s)'''
        list_of_var = [sub_time, title, message]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_answer(file, id_num):
    try:
        message, image = file
        query = '''
            INSERT INTO answer(submission_time, vote_number, question_id, message, image)
            VALUES (current_timestamp, 0, %s, %s, %s)'''
        list_of_var = [id_num, message, image]
    except ValueError:
        message = file[0]
        query = '''
            INSERT INTO answer(submission_time, vote_number, question_id, message)
            VALUES (current_timestamp, 0, %s, %s)'''
        list_of_var = [id_num, message]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_comment_to_question(message, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
    INSERT INTO comment(question_id, message, submission_time)
    VALUES (%s, %s, %s)'''
    list_of_var = [id_num, message, sub_time]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_comment_to_answer(message, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
    INSERT INTO comment(answer_id, message, submission_time)
    VALUES (%s, %s, %s)'''
    list_of_var = [id_num, message, sub_time]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_question(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image = file
        query = '''
            UPDATE question
            SET title = %s, message = %s, image = %s, submission_time = %s
            WHERE id = %s'''
        list_of_var = [title, message, image, sub_time, id_num]
    except ValueError:
        title, message = file
        query = '''
            UPDATE question
            SET title = %s, message = %s, submission_time = %s
            WHERE id = %s'''
        list_of_var = title, message, sub_time, id_num
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_comment(id_num, message):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
    UPDATE comment
    SET  message = %s, submission_time = %s
    WHERE id = %s'''
    list_of_var = [message, sub_time, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def delete_by_id(table, id_type, id_num):
    query = '''
    DELETE FROM %s
    WHERE %s = %s'''
    list_of_var = [table, id_type, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_answer(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        message, image = file
        query = '''
            UPDATE answer
            SET message = %s, image = %s, submission_time = %s
            WHERE id = %s'''
        list_of_var = [message, image, sub_time, id_num]
    except ValueError:
        message = file[0]
        query = '''
            UPDATE answer
            SET message = %s, submission_time = %s
            WHERE id = %s'''
        list_of_var = [message, sub_time, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def search_question(search):
    search = util.modify_search(search)
    search = '%' + search + '%'
    query = '''
    SELECT * FROM question
    WHERE title LIKE %s OR message LIKE %s '''
    list_of_var = [search, search]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def search_answer(search):
    search = util.modify_search(search)
    search = '%' + search + '%'
    print(search)
    query = """
    SELECT * FROM answer
    WHERE message LIKE %s ESCAPE '\'"""
    list_of_var = [search]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_tags(question_id):
    query = '''
        SELECT tag.name
        FROM question_tag
        INNER JOIN tag ON question_tag.tag_id=tag.id
        WHERE question_id = %s'''
    list_of_var = [question_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_tag_id(tag_name):
    query = '''
        SELECT id
        FROM tag
        WHERE name = %s'''
    list_of_var = [tag_name]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_tag_names():
    query = '''
        SELECT name
        FROM tag'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def modify_tags(question_id, new_tags):
    old_tags = [tag['name'] for tag in get_tags(question_id)]
    all_tags = [tag['name'] for tag in get_all_tag_names()]
    for tag in old_tags:
        if tag not in new_tags:
            tag_id = get_tag_id(tag)[0]['id']
            query = '''
            DELETE FROM question_tag
            WHERE question_id = %s AND tag_id = %s'''
            list_of_var = [question_id, tag_id]
            connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)
    for tag in new_tags:
        if tag not in old_tags:
            if tag not in all_tags:
                query = '''
                INSERT INTO tag (name)
                VALUES (%s)'''
                list_of_var = [tag]
                connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)
            tag_id = get_tag_id(tag)[0]['id']
            query = '''
            INSERT INTO question_tag(question_id, tag_id)
            VALUES (%s, %s)'''
            list_of_var = [question_id, tag_id]
            connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)
