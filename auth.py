from flask import Blueprint, render_template, request, redirect, url_for, session
from db import users_collection

auth = Blueprint('auth', __name__)

# ---------------- LOGIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            session['user'] = username
            return redirect(url_for('app_main'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


# ---------------- SIGNUP ----------------
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if users_collection.find_one({"username": username}):
            error = 'User already exists'
        else:
            users_collection.insert_one({
                "username": username,
                "password": password
            })
            session['user'] = username
            return redirect(url_for('app_main'))

    return render_template('signup.html', error=error)


# ---------------- LOGOUT ----------------
@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))