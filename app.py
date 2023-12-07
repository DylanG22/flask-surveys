from flask import Flask, request, render_template, flash, redirect, session
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Spaghetti&meAtballZ'

curr_survey = satisfaction_survey

@app.route('/')
def show_home_page():
    return render_template('home.html', title=curr_survey.title, instructions=curr_survey.instructions)


@app.route('/session',methods=['POST'])
def make_session():
    session['responses'] = []
    return redirect("/question/0")



@app.route('/question/<index>')
def show_question(index):
    i = int(index)
    if len(curr_survey.questions) == len(session['responses']):
        flash('Survey Already Somplete')
        return redirect('/survey_complete')
    elif i != len(session['responses']):
        flash('Invalid Question')
        return redirect(f'/question/{len(session["responses"])}')

    return render_template('question.html', q=curr_survey.questions[i], idx=i)

@app.route('/answer', methods=['POST'])
def handle_ans():
    req_list = list(request.form)
    i = req_list[0]
    ans = request.form[i]
    i = int(i)
    i+=1
    res = session['responses']
    res.append(ans)
    session['responses'] = res
    if i < len(curr_survey.questions):
        return redirect(f'/question/{i}')
    return redirect('/survey_complete')

@app.route('/survey_complete')
def survey_complete():
    print(session['responses'])
    return render_template('complete.html')