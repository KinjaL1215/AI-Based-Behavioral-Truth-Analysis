from flask import Blueprint, render_template, request, redirect, url_for, session
from db import users_collection
import bcrypt

auth = Blueprint('auth', __name__)

# ---------------- LOGIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None


    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')

        # Find user by email or username (do not check password here)
        user = users_collection.find_one({
            "$or": [
                {"email": login_input},
                {"username": login_input}
            ]
        })

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user'] = user.get('email')
            return redirect(url_for('app_main'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


# ---------------- SIGNUP ----------------
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None


    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Password strength check (server-side, in addition to HTML pattern)
        import re
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_pattern, password):
            error = 'Password must be at least 8 characters, include uppercase, lowercase, number, and special character.'
        elif users_collection.find_one({"email": email}):
            error = 'Email already registered.'
        elif users_collection.find_one({"username": username}):
            error = 'Username already taken.'
        else:
            # Hash the password before storing
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users_collection.insert_one({
                "email": email,
                "username": username,
                "password": hashed_pw
            })
            # After signup, redirect to login page instead of logging in automatically
            return redirect(url_for('auth.login'))

    return render_template('signup.html', error=error)


# ---------------- LOGOUT ----------------
@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))