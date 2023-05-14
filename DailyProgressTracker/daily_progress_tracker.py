import pytz
import os
import pyperclip
import ast
import tweepy
import datetime
from dotenv import load_dotenv
from textwrap import dedent
from flask import Flask, render_template, request, redirect, flash, send_from_directory, session

load_dotenv()
start_date = os.getenv('START_DATE')
markdown_file = os.getenv('MARKDOWN_FILE')
local_branch = os.getenv('LOCAL_BRANCH')
remote_branch = os.getenv('REMOTE_BRANCH')
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

IST = pytz.timezone('Asia/Kolkata')
today = datetime.datetime.now(IST)
start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") #type:ignore
start_date = IST.localize(start_date)
day_number = (today - start_date).days + 1
progress = int((day_number / 100) * 100)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def append_markdown():
    """Append markdown to file"""
    with open(markdown_file, "a") as f: #type:ignore
        f.write(session['markdown'] + "\n")

def push_to_github(file_name, local_branch, remote_branch):
    """Push file to Github"""
    print("\n-------------------Pushing to Github-------------------\n")
    script_location = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_location)

    os.system(f"git add ./DailyProgressTracker/{file_name}")
    os.system(f"git commit -m '{session['commit_message']}'")
    os.system(f"git push {local_branch} {remote_branch}")

def tweet_progress():
    """Tweet progress"""
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(session['tweet'])

def copy_to_clipboard():
    pyperclip.copy(session['tweet'].strip())

def generate_markdown_and_tweet(revised, solved):
    markdown_string = dedent(f"""
    ### Day {day_number}: {today.strftime('%B %dth, %Y')}

    **Today's Progress**
    """)
    tweet_string = dedent(f"""\n
    Day {day_number} of 100
    """)
    if revised != [''] and revised != []:
        markdown_string += "\nRevised:\n"
        markdown_string += "\n".join([f"- {topic}" for topic in revised])
        
        tweet_string += "\nRevised:\n"
        tweet_string += "\n".join([f"- {topic}" for topic in revised])
    
    if solved != [''] and solved != []:
        if revised != ['']:
            markdown_string += "\n"
            tweet_string += "\n"
        
        markdown_string += "\nSolved:\n"
        markdown_string += "\n".join([f"- [{q.split('.')[0].strip()}. {q.split('.')[1].strip()}](https://leetcode.com/problems/{q.split('.')[1].strip().lower().replace(' ','-')}/)" for q in solved])
        
        tweet_string += "\nSolved:\n"
        tweet_string += "\n".join([f"- {q.split('.')[0].strip()}. {q.split('.')[1].strip()}" for q in solved])
    
    tweet_string += "\n\n#100DaysOfCode"
    tweet_string = tweet_string.strip()
    
    commit_message = f"docs: 🚧 Day {day_number} - {' | '.join(revised)}"

    return markdown_string,tweet_string,commit_message

def submit():
    revised_topics = ast.literal_eval(request.form.getlist('revised')[0])
    solved_questions = ast.literal_eval(request.form.getlist('solved')[0])
    
    if (revised_topics == [] or revised_topics == ['']) and (solved_questions == [] or solved_questions == ['']):
        return False
    else:
        markdown, tweet, commit_message = generate_markdown_and_tweet(revised_topics, solved_questions)
        session['markdown'] = markdown
        session['tweet'] = tweet
        session['commit_message'] = commit_message
        return True

def check_session(item):
    if item not in session:
        flash('Please submit your progress first 😓', 'danger')
        return False
    else:
        return True

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html', progress=progress)

@app.route('/push-to-github')
def push_to_github_route():
    if check_session('commit_message'):
        push_to_github(markdown_file, local_branch, remote_branch)
        flash("Pushed logs to Github 💻", 'success')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/tweet-progress')
def tweet_progress_route():
    if check_session('tweet'):
        tweet_progress()
        flash('Tweeted progress 🐤', 'success')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/copy-to-clipboard')
def copy_to_clipboard_route():
    if check_session('tweet'):
        copy_to_clipboard()
        flash('Copied to clipboard 📜', 'success')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/generate-logs')
def generate_logs_route():
    if check_session('markdown'):
        append_markdown()
        flash('Generated logs 📝', 'success')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/submit', methods=['POST'])
def submit_route():
    result = submit()
    if result:
        flash('Your inputs have been submitted 🎉', 'success')
    else:
        flash('Please input values in the fields ❎', 'danger')
    return redirect('/')

@app.route('/clear-inputs')
def clear_inputs_route():
    flash('Cleared inputs 🫧', 'success')
    for key in list(session.keys()):
        session.pop(key, None)
    return render_template('index.html', progress=progress)

if __name__ == "__main__":
    app.run(debug=True, port=8000)