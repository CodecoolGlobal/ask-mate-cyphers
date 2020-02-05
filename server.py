import data_manager
import util
import os
import os.path
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


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


@app.route("/question/<question_id>/question")
@app.route("/question/<question_id>")
def route_question(question_id):
    if str(request.url_rule) == "/question/<question_id>":
        data_manager.vote("question", int(question_id), 1, "view_number")
    question = data_manager.get_question(int(question_id))
    tags = data_manager.get_tags(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comment = data_manager.get_comment('question_id', int(question_id))
    answers_comments = data_manager.get_all_comment()
    return render_template("question.html", question_id=int(question_id), question=question[0], answers=answers,
                           question_comment=question_comment, answers_comments=answers_comments, tags=tags)


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.add_question(file)
        questions = data_manager.get_all_questions_without_limit()
        new_id = 0
        for question in questions:
            if question['id'] > new_id:
                new_id = question['id']
        return redirect(f"/question/{new_id}")
    return render_template("ask_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_new_answer(question_id):
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.add_answer(file, int(question_id))
        return redirect(f"/question/{question_id}")
    question = data_manager.get_question(int(question_id))
    return render_template("post_answer.html", question=question, question_id=question_id)


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def route_question_comment(question_id):
    if request.method == "POST":
        file = request.form['message']
        data_manager.add_comment('question_id', file, int(question_id))
        return redirect(f"/question/{question_id}")
    question = data_manager.get_question(int(question_id))
    return render_template("question_comment.html", question=question, question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def route_answer_comment(answer_id):
    if request.method == "POST":
        answer = data_manager.get_answer(int(answer_id))
        file = request.form['message']
        data_manager.add_comment('answer_id', file, int(answer_id))
        return redirect(f"/question/{answer[0]['question_id']}")
    answer = data_manager.get_answer(int(answer_id))
    return render_template("answer_comment.html", answer=answer, answer_id=answer_id)


@app.route("/question/<question_id>/delete")
def route_question_delete(question_id):
    answers = data_manager.get_answers_by_question_id(int(question_id))
    question = data_manager.get_question(int(question_id))
    comments = data_manager.get_all_comment()
    for answer in answers:
        if os.path.exists(answer['image']):
            os.remove(answer['image'])
        for comment in comments:
            if answer['id'] == comment['answer_id']:
                data_manager.delete_by_id('comment', 'answer_id', int(comment['answer_id']))
    if os.path.exists(question[0]['image']):
        os.remove(question[0]['image'])
    data_manager.delete_by_id('question_tag', 'question_id', int(question_id))
    data_manager.delete_by_id('comment', 'question_id', int(question_id))
    data_manager.delete_by_id('answer', 'question_id', int(question_id))
    data_manager.delete_by_id('question', 'id', int(question_id))
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_question_edit(question_id):
    if request.method == "GET":
        question = data_manager.get_question(int(question_id))
        return render_template("edit_question.html", question=question, question_id=question_id)
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.edit_question(file, int(question_id))
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/<route>/vote_up")
def route_question_vote_up(question_id, route):
    data_manager.vote("question", int(question_id), 1, "vote_number")
    return redirect(f"/question/{question_id}/{route}")


@app.route("/question/<question_id>/<route>/vote_down")
def route_question_vote_down(question_id, route):
    data_manager.vote("question", int(question_id), -1, "vote_number")
    return redirect(f"/question/{question_id}/{route}")


@app.route("/answer/<answer_id>/delete")
def route_answer_delete(answer_id):
    answer = data_manager.get_answer(int(answer_id))
    if os.path.exists(answer[0]['image']):
        os.remove(answer[0]['image'])
    data_manager.delete_by_id('comment', 'answer_id', int(answer_id))
    data_manager.delete_by_id('answer', 'id', int(answer_id))
    return redirect(f"/question/{answer[0]['question_id']}")


@app.route("/comment/<comment_id>/delete")
def route_comment_delete(comment_id):
    comment = data_manager.get_comment('id', int(comment_id))
    data_manager.delete_by_id('comment', 'id', int(comment_id))
    if comment[0]['question_id'] is None:
        answer = data_manager.get_answer(int(comment[0]['answer_id']))
        comment = answer
    return redirect(f"/question/{comment[0]['question_id']}")


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    if request.method == 'GET':
        comment = data_manager.get_comment('id', int(comment_id))
        if comment[0]['question_id'] is None:
            answer = data_manager.get_answer(int(comment[0]['answer_id']))
            return render_template("edit_comment.html", comment=comment, answer=answer, comment_id=comment_id)
        else:
            return render_template("edit_comment.html", comment=comment, comment_id=comment_id, answer='')
    else:
        comment = data_manager.get_comment('id', int(comment_id))
        message = request.form['message']
        data_manager.edit_comment(int(comment_id), message)
        if comment[0]['question_id'] is None:
            answer = data_manager.get_answer(int(comment[0]['answer_id']))
            comment = answer
        return redirect(f'/question/{comment[0]["question_id"]}')


@app.route("/answer/<answer_id>/vote_up")
def route_answer_vote_up(answer_id):
    answer = data_manager.get_answer(int(answer_id))
    data_manager.vote("answer", int(answer_id), 1, "vote_number")
    return redirect(f"/question/{answer[0]['question_id']}")


@app.route("/answer/<answer_id>/vote_down")
def route_answer_vote_down(answer_id):
    answer = data_manager.get_answer(int(answer_id))
    data_manager.vote("answer", int(answer_id), -1, "vote_number")
    return redirect(f"/question/{answer[0]['question_id']}")


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_answer_edit(answer_id):
    if request.method == "GET":
        answer = data_manager.get_answer(answer_id)
        return render_template("edit_answer.html", answer=answer, answer_id=answer_id)
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.edit_answer(file, int(answer_id))
        answer = data_manager.get_answer(answer_id)
        return redirect(f"/question/{answer[0]['question_id']}")


@app.route("/search")
def route_search():
    search = request.args.get("search")
    questions = data_manager.search_question(search=search)
    answers = data_manager.search_answer(search=search)
    questions_with_answers = []
    for answer in answers:
        question_list = [data_manager.get_question(answer["question_id"])[0], answer]
        questions_with_answers.append(question_list)
    return render_template('search.html', questions=questions, answers=questions_with_answers, new_order_dir='desc', search=search)

                        
@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def route_tag_edit(question_id):
    if request.method == "GET":
        raw_tags = data_manager.get_tags(question_id)
        tags = ['#' + str(tag['name']) for tag in raw_tags]
        return render_template("new-tag.html", tags=tags, question_id=question_id)
    if request.method == "POST":
        new_tags = [request.form[item] for item in request.form]
        new_tags = new_tags[0].split()
        new_tags = [item.lstrip('#') for item in new_tags]
        data_manager.modify_tags(question_id, new_tags)
        return redirect(f"/question/{question_id}")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
