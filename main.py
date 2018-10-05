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
    p_verification_error = ''                      # {2}
    email_error = ''                               # {3}

    # retrieve form data
    u_candidate = request.form["username"]         # {4}
    p_candidate = request.form["password"]
    p_verified = request.form["password_verified"]
    e_candidate = request.form["email"]            # {5}

    # username validation
    if len(u_candidate) == 0:
        username_error = 'Please enter a username.'
    elif ' ' in u_candidate:
        username_error = 'cannot contain spaces.'
    elif len(u_candidate) < 3 or len(u_candidate) > 20:
        username_error = 'must be between 3 and 20 characters.'
    elif u_candidate.isalnum() == False:
        username_error = 'cannot contain special characters.'

    # password validation
    if len(p_candidate) == 0:
        password_error = 'Please enter a password.'
        p_candidate = ''
        p_verified = ''
    elif ' ' in p_candidate:
        password_error = 'cannot contain spaces.'
        p_candidate = ''
        p_verified = ''
    elif len(p_candidate) < 8 or len(p_candidate) > 20:
        password_error = 'must be between 8 and 20 characters.'
        p_candidate = ''
        p_verified = ''
    elif u_candidate in p_candidate or p_candidate in u_candidate:
        password_error = 'should not be similar to usernames.'
        p_candidate = ''
        p_verified = ''
    # password matching validation
    if p_candidate != p_verified:
        p_verification_error = 'Passwords do not match.'
        p_candidate = ''
        p_verified = ''

    # email validation
    if e_candidate == '':
        email_error = ''
    elif ' ' in e_candidate:
        email_error = 'cannot contain spaces.'
    elif len(u_candidate) < 3 or len(e_candidate) > 20:
        email_error = 'must be between 3 and 20 characters.'
    elif e_candidate.count("@") != 1:
        email_error = 'must contain 1 "@" symbol.'
    elif e_candidate.count(".") != 1:
        email_error = 'must contain 1 "." symbol.'

    # return errors or redirect if all input is valid
    if len(username_error + password_error + email_error + p_verification_error) == 0:
        #if all input is valid, redirect
        u_confirmed = u_candidate
        return redirect("/welcome?user=" + u_confirmed)
    else:
        return render_template('signup.html',
        username_error=username_error,
        password_error=password_error,
        p_verification_error=p_verification_error,
        email_error=email_error,
        u_candidate=u_candidate,
        e_candidate=e_candidate)

@app.route("/welcome")
def welcome():
    u_confirmed = request.args.get('user')
    return render_template('welcome.html', u_confirmed=u_confirmed)

app.run(debug = True)
