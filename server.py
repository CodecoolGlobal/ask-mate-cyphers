import data_manager
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list(order_by='id', order_direction='desc'):
    if request.args.get(order_by) is not None:
        order_by = request.args.get(order_by)
    if request.args.get(order_direction) is not None:
        order_direction = request.args.get(order_direction)
    questions = data_manager.get_all_questions(order_by, order_direction)
    headers = data_manager.get_headers()
    raw_headers = data_manager.HEADER_DATA
    return render_template('list.html', questions=questions, headers=headers, raw_headers=raw_headers)


@app.route("/question/<question_id>", methods=["GET", "POST"])
def route_question(question_id):
    return render_template("question.html")


# @app.route("/question/add-question")
# def route_add_question():
#     return "Hello World!"
#
#
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