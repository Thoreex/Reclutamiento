from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from reclutamiento.auth import login_required
from reclutamiento.db import get_conn, get_curs

def get_job(id):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT j.id, title, body, created_at, deleted_at, responsible_id, username, first_name, last_name'
        ' FROM tbl_job j'
        ' JOIN tbl_user u ON j.responsible_id = u.id'
        ' WHERE j.id = %s',
        (id,)
    )
    job = curs.fetchone()

    if job is None:
        abort(404, f"Job id {id} doesn't exist.")

    return job

bp = Blueprint('jobs', __name__)

@bp.route('/')
def index():
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT j.id, title, body, created_at, deleted_at, responsible_id, username, first_name, last_name'
        ' FROM tbl_job j'
        ' JOIN tbl_user u ON j.responsible_id = u.id'
        ' ORDER BY created_at DESC'
    )
    jobs = curs.fetchall()

    return render_template('jobs/index.html', jobs=jobs)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'INSERT INTO tbl_job (title, body, responsible_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            conn.commit()

            return redirect(url_for('jobs.index'))

    return render_template('jobs/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    job = get_job(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'UPDATE tbl_job SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            conn.commit()

            return redirect(url_for('jobs.index'))

    return render_template('jobs/update.html', job=job)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    get_job(id)

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('UPDATE tbl_job SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s', (id,))
    conn.commit()

    return redirect(url_for('jobs.index'))