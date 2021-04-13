import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
        )
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# creating blueprint named auth.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# the register view will return HTML with a form for users to fill out.
# When the user submit the form, the view will validate their input and
# either show the form again with an error message
# or create the new user and go to the login page.

# bp.route associates the URL /register with register view function. When
# flask receives a request for /auth/register, it will call register view
# and use the return value as response.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
                ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)
        if error is None:
            db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                    )
            # since db.execute is modifying data, db.commit needs to called to save changes.
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

# associates /login with the view function so that flask calls the function whenever it
# recieves request for /auth/login.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
                ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            # Session is a dictionary that holds data across requests.
            # When user logged in, user's id is stored in a new session.
            # The data is stored in a cookie that is sent to browser, and
            # then the browser sends it back with subsequent requests.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

# logout
# this make sure that the following function is called /auth/logout is request.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# user's id stored in session, will be available on subsequent requests.
# If user is logged in, their information should be loaded and made available
# to other views.
# this bp.before_app_request registers a function that needs to be run before any view function,
# no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
                ).fetchone()
# blogs require that user needs to be logged in.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

