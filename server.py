import data_manager
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/question/<question_id>/list")
@app.route("/list", methods=['GET', 'POST'])
def route_list(question_id=None, order_by=data_manager.DEFAULT_ORDER_BY, order_direction=data_manager.DEFAULT_ORDER_DIR):
    if request.args.get('order_by') is not None:
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
    questions = data_manager.get_all_questions(order_by, order_direction)
    headers = data_manager.get_headers()
    raw_headers = data_manager.HEADER_DATA
    new_order_dir = data_manager.get_new_order_dir(order_direction)
    questions = data_manager.get_time(questions)
    return render_template('list.html', questions=questions, headers=headers, raw_headers=raw_headers, new_order_dir=new_order_dir)


@app.route("/question/<question_id>/question")
@app.route("/question/<question_id>")
def route_question(question_id):
    questions = data_manager.get_all_questions()
    question = data_manager.get_row_for_id(int(question_id), questions)
    answers = data_manager.get_all_answers()
    data_manager.get_view_num(int(question_id))
    return render_template("question.html", question_id=question_id, question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.add_question(file)
        return redirect("/")
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
    questions = data_manager.get_all_questions()
    question = data_manager.get_row_for_id(int(question_id), questions)
    return render_template("post_answer.html", question=question, question_id=question_id)


@app.route("/question/<question_id>/delete")
def route_question_delete(question_id):
    data_manager.delete_question(question_id)
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_question_edit(question_id):
    if request.method == "GET":
        questions = data_manager.get_all_questions()
        question = data_manager.get_row_for_id(int(question_id), questions)
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
    data_manager.vote_up(int(question_id))
    return redirect(f"/question/{question_id}/{route}")


@app.route("/question/<question_id>/<route>/vote_down")
def route_question_vote_down(question_id, route):
    data_manager.vote_down(int(question_id))
    return redirect(f"/question/{question_id}/{route}")


@app.route("/answer/<answer_id>/delete")
def route_answer_delete(answer_id):
    answer = data_manager.get_row_for_id(answer_id, data_manager.get_all_answers())
    data_manager.delete_answer(answer_id)
    return redirect(f"/question/{answer['question_id']}")


@app.route("/answer/<answer_id>/vote_up")
def route_answer_vote_up(answer_id):
    answer = data_manager.get_row_for_id(answer_id, data_manager.get_all_answers())
    data_manager.answer_vote_up(int(answer_id))
    return redirect(f"/question/{answer['question_id']}")


@app.route("/answer/<answer_id>/vote_down")
def route_answer_vote_down(answer_id):
    answer = data_manager.get_row_for_id(answer_id, data_manager.get_all_answers())
    data_manager.answer_vote_down(int(answer_id))
    return redirect(f"/question/{answer['question_id']}")


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_answer_edit(answer_id):
    if request.method == "GET":
        answers = data_manager.get_all_answers()
        answer = data_manager.get_row_for_id(answer_id, answers)
        return render_template("edit_answer.html", answer=answer, answer_id=answer_id)
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join("static", image.filename))
            file.append(f"static/{image.filename}")
        data_manager.edit_answer(file, int(answer_id))
        answers = data_manager.get_all_answers()
        answer = data_manager.get_row_for_id(answer_id, answers)
        return redirect(f"/question/{answer['question_id']}")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
