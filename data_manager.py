import connection
import datetime
import util
import os


def get_user_id_by_id(table, question_id):
    query = '''
        SELECT user_id
        FROM {}
        WHERE id = %s'''.format(table)
    list_of_var = [question_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_questions_with_limit(order_by='id', desc='DESC'):
    query = '''
        SELECT q.id, q.submission_time, q.edit_submission_time, q.view_number, q.vote_number, q.title, q.message, q.image, q.user_id, u.username
        FROM question q
        JOIN users u on q.user_id = u.id
        ORDER BY {} {} LIMIT 5'''.format(order_by, desc)
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_questions_without_limit(order_by='id', desc='DESC'):
    query = '''
        SELECT q.id, q.submission_time, q.edit_submission_time, q.view_number, q.vote_number, q.title, q.message, q.image, q.user_id, u.username
        FROM question q
        JOIN users u on q.user_id = u.id
        ORDER BY {} {}'''.format(order_by, desc)
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_question_with_username(id_num):
    query = '''
        SELECT q.id, q.submission_time, q.edit_submission_time, q.view_number, q.vote_number, q.title, q.message, q.image, q.user_id, u.username
        FROM question q
        JOIN users u on q.user_id = u.id
        WHERE q.id = %s'''
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_answers_by_question_id(question_id):
    query = '''
        SELECT a.id, a.submission_time, a.edit_submission_time, a.vote_number, a.question_id, a.message, a.image, a.user_id, a.accepted, u.username
        FROM answer a
        JOIN users u on a.user_id = u.id
        WHERE question_id = %s
        ORDER BY id'''
    list_of_var = [question_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_row_from_table(table, id_num):
    query = '''
        SELECT *
        FROM {}
        WHERE id = %s'''.format(table)
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_comment_with_username(id_type, id_num):
    query = '''
        SELECT c.id, c.question_id, c.answer_id, c.message, c.submission_time, c.edit_submission_time, c.edited_count, c.user_id, u.username
        FROM comment c
        JOIN users u on c.user_id = u.id
        WHERE {} = %s'''.format(id_type)
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_answer_comments_with_username(q_id):
    query = '''
        SELECT c.id, c.question_id, c.answer_id, c.message, c.submission_time, c.edit_submission_time, c.edited_count, c.user_id, u.username
        FROM comment c
        JOIN users u on c.user_id = u.id
        WHERE answer_id IN (SELECT answer.id FROM answer WHERE answer.question_id = %s)'''
    list_of_var = [q_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_comment(id_type, id_num):
    query = '''
        SELECT *
        FROM comment
        WHERE {} = %s'''.format(id_type)
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_all_comment():
    query = '''
        SELECT *
        FROM comment'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def vote(table, id_num, num, column):
    query = '''
        UPDATE {}
        SET {} = {} + %s
        WHERE id = %s'''.format(table, column, column)
    list_of_var = [num, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_question(file):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image, user_id = file
        query = '''
            INSERT INTO question(submission_time, edit_submission_time, view_number, vote_number, title, message, image, user_id)
            VALUES (%s, %s, 0, 0, %s, %s, %s, %s)'''
        list_of_var = [sub_time, sub_time, title, message, image, user_id]
    except ValueError:
        title = file[0]
        message = file[1]
        user_id = file[2]
        query = '''
            INSERT INTO question(submission_time ,view_number, vote_number, title, message, edit_submission_time, user_id)
            VALUES (%s, 0, 0, %s, %s, %s, %s)'''
        list_of_var = [sub_time, title, message, sub_time, user_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_answer(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        message, image, user_id = file
        query = '''
            INSERT INTO answer(submission_time, vote_number, question_id, message, image, edit_submission_time, user_id)
            VALUES (%s, 0, %s, %s, %s, %s, %s)'''
        list_of_var = [sub_time, id_num, message, image, sub_time, user_id]
    except ValueError:
        message = file[0]
        user_id = file[1]
        query = '''
            INSERT INTO answer(submission_time, vote_number, question_id, message, edit_submission_time, user_id)
            VALUES (%s, 0, %s, %s, %s, %s)'''
        list_of_var = [sub_time, id_num, message, sub_time, user_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_comment_to_question(message, q_id_num, user_id):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
        INSERT INTO comment(question_id, message, submission_time, edit_submission_time, user_id)
        VALUES (%s, %s, %s, %s, %s)'''
    list_of_var = [q_id_num, message, sub_time, sub_time, user_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def add_comment_to_answer(message, q_id_num, user_id):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
        INSERT INTO comment(answer_id, message, submission_time, edit_submission_time, user_id)
        VALUES (%s, %s, %s, %s, %s)'''
    list_of_var = [q_id_num, message, sub_time, sub_time, user_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_question(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        title, message, image = file
        query = '''
            UPDATE question
            SET title = %s, message = %s, image = %s, edit_submission_time = %s
            WHERE id = %s'''
        list_of_var = [title, message, image, sub_time, id_num]
    except ValueError:
        title, message = file
        query = '''
            UPDATE question
            SET title = %s, message = %s, edit_submission_time = %s
            WHERE id = %s'''
        list_of_var = [title, message, sub_time, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_comment(id_num, message):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
        UPDATE comment
        SET  message = %s, edit_submission_time = %s, edited_count = edited_count + 1
        WHERE id = %s'''
    list_of_var = [message, sub_time, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def delete_by_id(table, id_type, id_num):
    query = '''
        DELETE FROM {}
        WHERE {} = %s'''.format(table, id_type)
    list_of_var = [id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def delete_image(table, image):
    query = """
    UPDATE {}
    SET image = '{}'
    WHERE image = '{}'""".format(table, 'None', image)
    list_of_var = []
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def edit_answer(file, id_num):
    sub_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        message, image = file
        query = '''
            UPDATE answer
            SET message = %s, image = %s, edit_submission_time = %s
            WHERE id = %s'''
        list_of_var = [message, image, sub_time, id_num]
    except ValueError:
        message = file[0]
        query = '''
            UPDATE answer
            SET message = %s, edit_submission_time = %s
            WHERE id = %s'''
        list_of_var = [message, sub_time, id_num]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def search_question(search):
    search = util.modify_search(search)
    search = '%' + search + '%'
    query = '''
        SELECT q.id, q.submission_time, q.edit_submission_time, q.view_number, q.vote_number, q.title, q.message, q.image, q.user_id, u.username
        FROM question q 
        JOIN users u ON u.id = q.user_id 
        WHERE title ILIKE %s OR message ILIKE %s '''
    list_of_var = [search, search]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def search_answer(search):
    search = util.modify_search(search)
    search = '%' + search + '%'
    query = """
        SELECT a.id, a.submission_time, a.edit_submission_time, a.vote_number, a.question_id, a.message, a.image, a.user_id, a.accepted, u.username
        FROM answer a 
        JOIN users u ON u.id = a.user_id
        WHERE message ILIKE %s"""
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


def get_all_tag_names():
    query = '''
        SELECT name
        FROM tag'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def modify_tags(question_id, new_tags):
    for tag in new_tags:
        query = '''
            INSERT INTO tag (name)
            SELECT %s
            WHERE NOT EXISTS (SELECT name FROM tag WHERE name = %s);
            INSERT INTO question_tag(question_id, tag_id)
            SELECT %s, (SELECT id FROM tag WHERE name = %s)
            WHERE NOT EXISTS (SELECT question_id, tag_id FROM question_tag 
            WHERE question_id = %s and tag_id = (SELECT id FROM tag WHERE name = %s))'''
        list_of_var = [tag, tag, question_id, tag, question_id, tag]
        connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def get_name_of_image(filename):
    i = 1
    while True:
        if os.path.exists(f"static/{filename}"):
            print(filename)
            filename = filename + str(i)
            i += 1
        else:
            return filename


def get_question_id_from_tag_id(tag_id):
    query = '''
        SELECT question_id
        FROM question_tag
        WHERE tag_id=%s'''
    list_of_var = [tag_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_whole_tags(tag_name):
    query = '''
        SELECT question_id
        FROM question_tag
        RIGHT JOIN tag ON question_tag.tag_id=tag.id
        WHERE tag.name = %s'''
    list_of_var = [tag_name]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_password(username):
    query = '''
        SELECT password
        FROM users
        WHERE username = %s'''
    list_of_var = [username]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def add_new_user(list_of_data):
    username, email_address, password = list_of_data
    registration_date = datetime.datetime.now().replace(microsecond=0).isoformat()
    query = '''
        INSERT INTO users(username, email_address, registration_date, password)
        VALUES (%s, %s, %s, %s)'''.format(registration_date)
    list_of_var = [username, email_address, registration_date, password]
    return connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def get_user_id(username):
    query = '''
        SELECT id
        FROM users
        WHERE username = %s'''
    list_of_var = [username]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_user_name_by_id(id_num):
    query = '''
        SELECT username
        FROM users
        WHERE id = %s'''
    list_of_var = [id_num]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_users():
    query = '''
        SELECT u.id, 
        username,
        registration_date,
        (SELECT count(*) FROM question WHERE user_id = u.id) AS count_of_asked,
        (SELECT COUNT(*) FROM answer WHERE user_id = u.id) AS count_of_answers,
        (SELECT COUNT(*) FROM comment WHERE user_id = u.id) AS count_of_comments,
        reputation
        FROM users u
        GROUP BY u.id'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_data_by_user_id(table_name, user_id):
    query = '''
        SELECT *
        FROM {}
        WHERE user_id = %s'''.format(table_name)
    list_of_var = [user_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def get_user(user_id):
    query = '''
        SELECT u.id, 
        username,
        registration_date,
        (SELECT count(*) FROM question WHERE user_id = u.id) AS count_of_asked,
        (SELECT COUNT(*) FROM answer WHERE user_id = u.id) AS count_of_answers,
        (SELECT COUNT(*) FROM comment WHERE user_id = u.id) AS count_of_comments,
        reputation
        FROM users u
        WHERE id = %s
        GROUP BY u.id'''
    list_of_var = [user_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def user_vote_saving(column, vote_id, u_id, value):
    query = '''
        INSERT INTO votes ({}, user_id, updown)
        VALUES (%s, %s, %s)'''.format(column)
    list_of_var = [vote_id, u_id, value]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def check_if_user_voted_question(question_id, u_id, value):
    query = '''
        SELECT *
        FROM votes
        WHERE question_id = %s AND user_id = %s AND updown = %s'''
    list_of_var = [question_id, u_id, value]
    if connection.db_mod_list_with_return(query=query, list_of_var=list_of_var):
        return True
    return False


def check_if_user_voted_answer(answer_id, u_id, value):
    query = '''
        SELECT *
        FROM votes
        WHERE answer_id = %s AND user_id = %s AND updown = %s'''
    list_of_var = [answer_id, u_id, value]
    if connection.db_mod_list_with_return(query=query, list_of_var=list_of_var):
        return True
    return False


def vote_value(id_type, id_num, u_id):
    query = '''
        SELECT updown
        FROM votes
        WHERE {} = %s AND user_id = %s'''.format(id_type)
    list_of_var = [id_num, u_id]
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def delete_vote(id_type, id_num, u_id):
    query = '''
        DELETE FROM votes
        WHERE {} = %s AND user_id = %s'''.format(id_type)
    list_of_var = [id_num, u_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def change_answer_accepted(answer_id, value):
    query = '''
        UPDATE answer
        SET accepted = %s
        WHERE id = %s'''
    list_of_var = [value, answer_id]
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)


def get_tags_data():
    query = '''
        SELECT t.name as name,
        (SELECT COUNT(*) FROM question_tag WHERE tag_id = t.id) as count_of_marked FROM tag t
        GROUP BY t.name, t.id
        ORDER BY count_of_marked'''
    list_of_var = []
    return connection.db_mod_list_with_return(query=query, list_of_var=list_of_var)


def check_user_data(column, data):
    query = '''
        SELECT {}
        FROM users
        WHERE {} = %s'''.format(column, column)
    list_of_var = [data]
    if connection.db_mod_list_with_return(query=query, list_of_var=list_of_var):
        return True
    return False


def tag_delete():
    query = '''
        DELETE FROM tag t
        WHERE t.id not in (SELECT tag_id FROM question_tag)'''
    list_of_var = []
    connection.db_mod_list_without_return(query=query, list_of_var=list_of_var)
