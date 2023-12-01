from flask import Flask, request, render_template, flash, redirect
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)

responses = []

curr_survey = satisfaction_survey

@app.route('/')
def show_home_page():
    return render_template('home.html', title=curr_survey.title, instructions=curr_survey.instructions)

@app.route('/question/<index>')
def show_question(index):
    i = int(index)
    if i != len(responses):
        flash('Invalid Question')
        return redirect(f'/question/{len(responses)}')
    elif len(curr_survey.questions) == len(responses):
        flash('Survey Already Somplete')
        return redirect('/survey_complete')
    return render_template('question.html', q=curr_survey.questions[i], idx=i)

@app.route('/answer', methods=['POST'])
def handle_ans():
    req_list = list(request.form)
    i = req_list[0]
    ans = request.form[i]
    print(i,ans,type(ans))
    i = int(i)
    i+=1
    responses.append(ans)
    if i < len(curr_survey.questions):
        return redirect(f'/question/{i}')
    return redirect('/survey_complete')

@app.route('/survey_complete')
def survey_complete():
    return render_template('complete.html')