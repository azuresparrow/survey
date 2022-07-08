from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "supersecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def default_route():
    return render_template("home.html", survey_title=survey.title)

@app.route('/questions/<int:id>')
def question(id):
    responses = session.get(RESPONSES_KEY)
    if(responses is None):
        return redirect("/")
    elif len(responses) == len(survey.questions):
        flash(f"Survey is already complete")
        return redirect('/complete')
    elif len(responses) != id:
        flash(f"Invalid question - {id}")
        return redirect(f'/questions/{len(responses)}')
    elif id < len(survey.questions):
        return render_template("question.html", question=survey.questions[id])

@app.route('/answer', methods=["POST"])
def handle_response():
    choice = request.form["option"]
    responses = session.get(RESPONSES_KEY)
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/complete')

@app.route('/start')
def start_new_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/complete')
def finished_survey():
    return render_template("complete.html")