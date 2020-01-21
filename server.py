import data_manager
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list(order_by='id', order_direction='desc'):
    if request.method == 'GET':
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
    questions = data_manager.get_all_questions(order_by, order_direction)
    headers = data_manager.get_headers()
    raw_headers = data_manager.HEADER_DATA
    new_order_dir = data_manager.get_new_order_dir(order_direction)
    return render_template('list.html', questions=questions, headers=headers, raw_headers=raw_headers, new_order_dir=new_order_dir)



@app.route("/question/<question_id>")
def route_question(question_id):
    questions = data_manager.get_all_questions()
    answers = data_manager.get_all_answers()
    return render_template("question.html", question_id=question_id, questions=questions, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    if request.method == "POST":
        file = [request.form[item] for item in request.form]
        data_manager.add_question(file)
        return redirect("/")
    return render_template("ask_question.html")


# @app.route("/question/<question_id>/new-answer")
# def route_new_answer():
#     return "Hello World!"
#
#
# @app.route("/question/<question_id>/delete")
# def route_question_delete():
#     return "Hello World!"
#
#
# @app.route("/question/<question_id>/edit")
# def route_question_edit():
#     return "Hello World!"
#
#
# @app.route("/answer/<answer_id>delete")
# def route_question_delete():
#     return "Hello World!"
#
#
# @app.route("/question/<question_id>/vote_up")
# def route_question_vote_up():
#     return "Hello World!"
#
#
# @app.route("/question/<question_id>/vote_down")
# def route_question_vote_up():
#     return "Hello World!"
#
#
# @app.route("/question/<answer_id>/vote_up")
# def route_answer_vote_up():
#     return "Hello World!"
#
#
# @app.route("/question/<answer_id>/vote_down")
# def route_answer_vote_up():
#     return "Hello World!"


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )