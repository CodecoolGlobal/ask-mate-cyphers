import data_manager
import util
import os
import os.path
from flask import Flask, render_template, request, redirect, flash, session, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def route_main(question_id=None, order_by="id", order_direction="desc"):
    if request.args.get('order_by') is not None:
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        order_direction = util.get_new_order_dir(order_direction)
    questions = data_manager.get_all_questions_with_limit(order_by, order_direction)
    return render_template('list.html', questions=questions, new_order_dir=order_direction)


@app.route("/question/<question_id>/list")
@app.route("/list", methods=['GET', 'POST'])
def route_list(question_id=None, order_by="id", order_direction="desc"):
    if request.args.get('order_by') is not None:
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        order_direction = util.get_new_order_dir(order_direction)
    questions = data_manager.get_all_questions_without_limit(order_by, order_direction)
    return render_template('list.html', questions=questions, new_order_dir=order_direction)


@app.route("/question/<question_id>")
def route_question_view(question_id):
    question = data_manager.get_row_from_table('question', question_id)[0]
    if 'id' in session and session["id"] != question["user_id"]:
        data_manager.vote("question", int(question_id), 1, "view_number")
    return redirect(f"/question/{question_id}/question")


@app.route("/question/<question_id>/question")
def route_question(question_id):
    question = data_manager.get_question_with_username(int(question_id))
    tags = data_manager.get_tags(question_id)
    answers = data_manager.get_answers_by_question_id(int(question_id))
    question_comment = data_manager.get_comment_with_username('question_id', int(question_id))
    answers_comments = data_manager.get_answer_comments_with_username(int(question_id))
    return render_template("question.html", question_id=int(question_id), question=question[0], answers=answers,
                           question_comment=question_comment, answers_comments=answers_comments, tags=tags)


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            filename = data_manager.get_name_of_image(image.filename)
            image.save(os.path.join("static", filename))
            file.append(f"/static/{filename}")
        file.append(session['id'])
        data_manager.add_question(file)
        questions = data_manager.get_all_questions_without_limit()
        new_id = 0
        for question in questions:
            if question['id'] > new_id:
                new_id = question['id']
        return redirect(f"/question/{new_id}/question")
    return render_template("ask_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_new_answer(question_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            filename = data_manager.get_name_of_image(image.filename)
            image.save(os.path.join("static", filename))
            file.append(f"/static/{filename}")
        file.append(session['id'])
        data_manager.add_answer(file, int(question_id))
        return redirect(f"/question/{question_id}/question")
    question = data_manager.get_row_from_table('question', int(question_id))
    return render_template("post_answer.html", question=question, question_id=question_id)


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def route_question_comment(question_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "POST":
        file = request.form['message']
        data_manager.add_comment_to_question(file, int(question_id), session['id'])
        return redirect(f"/question/{question_id}/question")
    question = data_manager.get_row_from_table('question', int(question_id))
    return render_template("question_comment.html", question=question, question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def route_answer_comment(answer_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "POST":
        answer = data_manager.get_row_from_table('answer', int(answer_id))
        file = request.form['message']
        data_manager.add_comment_to_answer(file, int(answer_id), session['id'])
        return redirect(f"/question/{answer[0]['question_id']}/question")
    answer = data_manager.get_row_from_table('answer', int(answer_id))
    return render_template("answer_comment.html", answer=answer, answer_id=answer_id)


@app.route("/question/<question_id>/delete")
def route_question_delete(question_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    answers = data_manager.get_answers_by_question_id(int(question_id))
    question = data_manager.get_row_from_table('question', int(question_id))
    for answer in answers:
        if os.path.exists(answer['image'][1:]):
            os.remove(answer['image'][1:])
    if os.path.exists(question[0]['image'][1:]):
        os.remove(question[0]['image'][1:])
    data_manager.delete_by_id('question', 'id', int(question_id))
    data_manager.tag_delete()
    return redirect("/")


@app.route("/delete/question/<question_id>", methods=['POST'])
def image_delete_from_question(question_id):
    if request.method == 'POST':
        image = request.form['image']
        data_manager.delete_image('question', image)
        if os.path.exists(image[:1]):
            os.remove(image[1:])
        return redirect(f"/question/{question_id}/edit")


@app.route("/delete/answer/<answer_id>", methods=['POST'])
def image_delete_from_answer(answer_id):
    if request.method == 'POST':
        image = request.form['image']
        data_manager.delete_image('answer', image)
        if os.path.exists(image[:1]):
            os.remove(image[1:])
        return redirect(f"/answer/{answer_id}/edit")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_question_edit(question_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "GET":
        question = data_manager.get_row_from_table('question', int(question_id))
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            filename = data_manager.get_name_of_image(image.filename)
            image.save(os.path.join("static", filename))
            file.append(f"/static/{image.filename}")
        data_manager.edit_question(file, int(question_id))
        return redirect(f"/question/{question_id}/question")


@app.route("/question/<question_id>/<route>/vote_up")
def route_question_vote_up(question_id, route):
    owner_id = data_manager.get_user_id_by_id('question', int(question_id))[0]['user_id']
    if 'id' in session and session["id"] != owner_id:
        if data_manager.check_if_user_voted_question(int(question_id), int(session["id"]), 'True'):
            data_manager.vote("question", int(question_id), -1, "vote_number")
            data_manager.vote('users', int(owner_id), -5, 'reputation')
            data_manager.delete_vote('question_id', int(question_id), session['id'])
        elif data_manager.check_if_user_voted_question(int(question_id), int(session["id"]), 'False'):
            data_manager.vote('question', int(question_id), 2, 'vote_number')
            data_manager.vote('users', int(owner_id), 7, 'reputation')
            data_manager.delete_vote('question_id', int(question_id), session['id'])
            data_manager.user_vote_saving('question_id', question_id, int(session["id"]), 'True')
        else:
            data_manager.vote("question", int(question_id), 1, "vote_number")
            data_manager.vote('users', int(owner_id), 5, 'reputation')
            data_manager.user_vote_saving('question_id', question_id, int(session["id"]), 'True')
    return redirect(f"/question/{question_id}/{route}")


@app.route("/question/<question_id>/<route>/vote_down")
def route_question_vote_down(question_id, route):
    owner_id = data_manager.get_user_id_by_id('question', int(question_id))[0]['user_id']
    if 'id' in session and session["id"] != owner_id:
        if data_manager.check_if_user_voted_question(int(question_id), int(session["id"]), 'False'):
            data_manager.vote("question", int(question_id), 1, "vote_number")
            data_manager.vote('users', int(owner_id), 2, 'reputation')
            data_manager.delete_vote('question_id', int(question_id), session['id'])
        elif data_manager.check_if_user_voted_question(int(question_id), int(session["id"]), 'True'):
            data_manager.vote('question', int(question_id), -2, 'vote_number')
            data_manager.vote('users', int(owner_id), -7, 'reputation')
            data_manager.delete_vote('question_id', int(question_id), session['id'])
            data_manager.user_vote_saving('question_id', question_id, int(session["id"]), 'False')
        else:
            data_manager.vote("question", int(question_id), -1, "vote_number")
            data_manager.vote('users', int(owner_id), -2, 'reputation')
            data_manager.user_vote_saving('question_id', question_id, int(session["id"]), 'False')
    return redirect(f"/question/{question_id}/{route}")


@app.route("/answer/<answer_id>/vote_up")
def route_answer_vote_up(answer_id):
    owner_id = data_manager.get_user_id_by_id('answer', int(answer_id))[0]['user_id']
    if 'id' in session and int(session["id"]) != owner_id:
        if data_manager.check_if_user_voted_answer(int(answer_id), int(session["id"]), 'True'):
            data_manager.vote("answer", int(answer_id), -1, "vote_number")
            data_manager.vote('users', int(owner_id), -10, 'reputation')
            data_manager.delete_vote('answer_id', int(answer_id), session['id'])
        elif data_manager.check_if_user_voted_answer(int(answer_id), int(session["id"]), 'False'):
            data_manager.vote("answer", int(answer_id), 2, "vote_number")
            data_manager.vote('users', int(owner_id), 12, 'reputation')
            data_manager.delete_vote('answer_id', int(answer_id), session['id'])
            data_manager.user_vote_saving('answer_id', int(answer_id), int(session['id']), 'True')
        else:
            data_manager.vote("answer", int(answer_id), 1, "vote_number")
            data_manager.vote('users', int(owner_id), 10, 'reputation')
            data_manager.user_vote_saving('answer_id', answer_id, int(session["id"]), 'True')
    answer = data_manager.get_row_from_table('answer', int(answer_id))
    return redirect(f"/question/{answer[0]['question_id']}/question")


@app.route("/answer/<answer_id>/vote_down")
def route_answer_vote_down(answer_id):
    owner_id = data_manager.get_user_id_by_id('answer', int(answer_id))[0]['user_id']
    if 'id' in session and int(session["id"]) != owner_id:
        if data_manager.check_if_user_voted_answer(int(answer_id), int(session["id"]), 'False'):
            data_manager.vote("answer", int(answer_id), 1, "vote_number")
            data_manager.vote('users', int(owner_id), 2, 'reputation')
            data_manager.delete_vote('answer_id', int(answer_id), session['id'])
        elif data_manager.check_if_user_voted_answer(int(answer_id), int(session["id"]), 'True'):
            data_manager.vote("answer", int(answer_id), -2, "vote_number")
            data_manager.vote('users', int(owner_id), -12, 'reputation')
            data_manager.delete_vote('answer_id', int(answer_id), session['id'])
            data_manager.user_vote_saving('answer_id', int(answer_id), int(session['id']), 'False')
        else:
            data_manager.vote("answer", int(answer_id), -1, "vote_number")
            data_manager.vote('users', int(owner_id), -2, 'reputation')
            data_manager.user_vote_saving('answer_id', answer_id, int(session["id"]), False)
    answer = data_manager.get_row_from_table('answer', int(answer_id))
    return redirect(f"/question/{answer[0]['question_id']}/question")


@app.route("/answer/<answer_id>/delete")
def route_answer_delete(answer_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    answer = data_manager.get_row_from_table('answer', int(answer_id))
    if os.path.exists(answer[0]['image'][1:]):
        os.remove(answer[0]['image'][1:])
    data_manager.delete_by_id('answer', 'id', int(answer_id))
    return redirect(f"/question/{answer[0]['question_id']}/question")


@app.route("/comment/<comment_id>/delete")
def route_comment_delete(comment_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    comment = data_manager.get_comment('id', int(comment_id))
    data_manager.delete_by_id('comment', 'id', int(comment_id))
    if comment[0]['question_id'] is None:
        answer = data_manager.get_row_from_table('answer', int(comment[0]['answer_id']))
        comment = answer
    return redirect(f"/question/{comment[0]['question_id']}/question")


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == 'GET':
        comment = data_manager.get_comment('id', int(comment_id))
        if comment[0]['question_id'] is None:
            answer = data_manager.get_row_from_table('answer', int(comment[0]['answer_id']))
            return render_template("edit_comment.html", comment=comment, answer=answer, comment_id=comment_id)
        else:
            return render_template("edit_comment.html", comment=comment, comment_id=comment_id, answer='')
    else:
        comment = data_manager.get_comment('id', int(comment_id))
        message = request.form['message']
        data_manager.edit_comment(int(comment_id), message)
        if comment[0]['question_id'] is None:
            answer = data_manager.get_row_from_table('answer', int(comment[0]['answer_id']))
            comment = answer
        return redirect(f'/question/{comment[0]["question_id"]}/question')


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_answer_edit(answer_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "GET":
        answer = data_manager.get_row_from_table('answer', answer_id)
        return render_template("edit_answer.html", answer=answer, answer_id=answer_id)
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            filename = data_manager.get_name_of_image(image.filename)
            image.save(os.path.join("static", filename))
            file.append(f"/static/{image.filename}")
        data_manager.edit_answer(file, int(answer_id))
        answer = data_manager.get_row_from_table('answer', answer_id)
        return redirect(f"/question/{answer[0]['question_id']}/question")


@app.route("/search/<tag>")
@app.route("/search")
def route_search(tag=None):
    if tag is None:
        search = request.args.get("search")
        questions = data_manager.search_question(search=search)
        answers = data_manager.search_answer(search=search)
        questions_with_answers = []
        for answer in answers:
            question_list = [data_manager.get_row_from_table('question', answer["question_id"])[0], answer]
            questions_with_answers.append(question_list)
        return render_template('search.html', questions=questions, answers=questions_with_answers, search=search)
    else:
        list_of_question_id = data_manager.get_whole_tags(tag_name=tag)
        questions = []
        if list_of_question_id[0]['question_id'] is not None:
            for i in list_of_question_id:
                question = data_manager.get_row_from_table('question', i["question_id"])[0]
                questions.append(question)
        return render_template('search.html', questions=questions, answers=None, search=tag)


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def route_tag_edit(question_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    if request.method == "GET":
        raw_tags = data_manager.get_tags(question_id)
        tags = ['#' + str(tag['name']) for tag in raw_tags]
        return render_template("new-tag.html", tags=tags, question_id=question_id)
    if request.method == "POST":
        new_tags = [request.form[item] for item in request.form]
        new_tags = new_tags[0].split()
        new_tags = [item.lstrip('#') for item in new_tags]
        data_manager.modify_tags(question_id, new_tags)
        return redirect(f"/question/{question_id}/question")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        req = request.form
        hashed_password = util.hash_password(req['password'])
        if data_manager.check_user_data('username', req['username']) is True:
            flash('This username is already taken!')
            return redirect(request.url)
        elif data_manager.check_user_data('email_address', req['email']) is True:
            flash('This email address is already taken!')
            return redirect(request.url)
        elif len(req['password']) < 7:
            flash('Too short password! (Min. 7 character.)')
            return redirect(request.url)
        elif not util.verify_password(req['password_again'], hashed_password):
            flash('The passwords are different!')
            return redirect(request.url)
        else:
            list_of_data = [req['username'], req['email'], util.hash_password(req['password'])]
            data_manager.add_new_user(list_of_data)
            session['id'] = data_manager.get_user_id(req['username'])[0]['id']
            session['username'] = req['username']
            return redirect(url_for('route_main'))
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id' in session:
        return redirect(url_for('route_main'))
    if request.method == 'POST':
        req = request.form
        try:
            if not util.verify_password(req['password'], data_manager.get_password(req['username'])[0]['password']):
                flash('Incorrect password or username!')
                return redirect(request.url)
            else:
                session['id'] = data_manager.get_user_id(req['username'])[0]['id']
                session['username'] = req['username']
                return redirect(url_for('route_main'))
        except IndexError:
            flash('Incorrect Username!')
            return redirect(request.url)
    return render_template('login.html')


@app.route('/answer/<answer_id>/accept/<value>')
def route_answer_accept_change(answer_id, value):
    answer = data_manager.get_row_from_table('answer', answer_id)
    value = util.change_boolean_value(value)
    if value:
        data_manager.vote('users', int(answer[0]["user_id"]), 15, 'reputation')
    else:
        data_manager.vote('users', int(answer[0]["user_id"]), -15, 'reputation')
    data_manager.change_answer_accepted(int(answer_id), value)
    return redirect(f"/question/{answer[0]['question_id']}/question")


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('route_main'))


@app.route('/users')
def list_users():
    if 'id' not in session:
        return redirect(url_for('route_main'))
    users = data_manager.get_users()
    return render_template('list_users.html', users=users)


@app.route('/user/<user_id>')
def user_page(user_id):
    if 'id' not in session:
        return redirect(url_for('route_main'))
    user = data_manager.get_user(user_id)
    questions = data_manager.get_data_by_user_id('question', user_id)
    answers = data_manager.get_data_by_user_id('answer', user_id)
    comments = data_manager.get_data_by_user_id('comment', user_id)
    return render_template('user_page.html', user=user[0], questions=questions, answers=answers, comments=comments)


@app.route('/tags')
def tags_data():
    tags = data_manager.get_tags_data()
    return render_template('tags.html', tags=tags)


@app.route('/answer/comment/<answer_id>')
def route_from_comment_to_question(answer_id):
    answer = data_manager.get_row_from_table('answer', int(answer_id))
    return redirect(f"/question/{answer[0]['question_id']}")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
