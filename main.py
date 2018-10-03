from flask import Flask, request, redirect, render_template
import os
import string

app = Flask(__name__)

def is_in(symbols, candidate):
    found = ''

    for char in symbols:
        if char in candidate:
            found += char

    if len(found) > 0:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('signup.html')

@app.route("/", methods=['POST'])
def validate():
    username_error = ''                            # {0}
    password_error = ''                            # {1}
    email_error = ''                               # {2}

    u_candidate = request.form["username"]         # {3}
    p_candidate = request.form["password"]
    p_verified = request.form["password_verified"]
    e_candidate = request.form["email"]            # {4}

    if len(u_candidate) == 0:
        username_error = 'Please enter a username.'
    elif ' ' in u_candidate:
        username_error = 'Usernames cannot contain spaces.'
    elif len(u_candidate) < 3 or len(u_candidate) > 20:
        username_error = 'Usernames must be between 3 and 20 characters.'
    elif u_candidate.isalnum() == False:
        username_error = 'Usernames cannot contain special characters.'

    if len(username_error + password_error + email_error) == 0:
        #if all input is valid, redirect
        u_confirmed = u_candidate
        return redirect("/welcome?user=" + u_confirmed)
    else:
        return render_template('signup.html',
        username_error=username_error,
        password_error=password_error,
        email_error=email_error,
        u_candidate=u_candidate,
        e_candidate=e_candidate)

@app.route("/welcome")
def welcome():
    u_confirmed = request.args.get('user')
    return render_template('welcome.html', u_confirmed=u_confirmed)

app.run(debug = True)
