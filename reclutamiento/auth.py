import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from reclutamiento.db import get_conn, get_curs

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_conn()
        curs = get_curs(conn)

        curs.execute(
            'SELECT id, username, password, first_name, last_name, is_admin FROM tbl_user WHERE id = %s', (user_id,)
        )
        g.user = curs.fetchone()

        curs.close()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        conn = get_conn()

        if error is None:
            try:
                curs = get_curs(conn)

                curs.execute(
                    "INSERT INTO tbl_user (username, password, first_name, last_name) VALUES (%s, %s, %s, %s)",
                    (username, generate_password_hash(password), first_name, last_name),
                )
                conn.commit()

                curs.close()
            except conn.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        conn = get_conn()
        curs = get_curs(conn)

        curs.execute(
            'SELECT id, username, password, first_name, last_name, is_admin FROM tbl_user WHERE username = %s', (username,)
        )
        user = curs.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))