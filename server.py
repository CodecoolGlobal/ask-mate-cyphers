from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_list():
    return "Hello World!"


@app.route("/question/<question_id>")
def route_question():
    return "Hello World!"


@app.route("/question/add-question")
def route_question():
    return "Hello World!"


@app.route("/question/<question_id>/new-answer")
def route_question():
    return "Hello World!"


@app.route("/question/<question_id>/delete")
def route_question():
    return "Hello World!"


@app.route("/question/<question_id>/edit")
def route_question():
    return "Hello World!"


@app.route("/answer/<answer_id>delete")
def route_question():
    return "Hello World!"


@app.route("/question/<question_id>/vote_up")
def route_question():
    return "Hello World!"


@app.route("/question/<question_id>/vote_down")
def route_question():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
