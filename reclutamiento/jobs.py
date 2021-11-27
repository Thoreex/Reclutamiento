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

    curs.close()

    if job is None:
        abort(404, f"Job id {id} doesn't exist.")

    return job

def get_application(applicant_id, job_id, check_owner=True):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT id, applicant_id, job_id, application_date'
        ' FROM tbl_application'
        ' WHERE applicant_id = %s and job_id = %s',
        (applicant_id, job_id)
    )
    application = curs.fetchone()

    curs.close()

    if application is None:
        abort(404, f"Job id {id} doesn't exist.")

    if check_owner and application['applicant_id'] != g.user['id']:
        abort(403)

    return application

bp = Blueprint('jobs', __name__)

@bp.route('/')
def index():
    conn = get_conn()
    curs = get_curs(conn)

    if (g.user is None):
        curs.execute(
            'SELECT j.id, j.title, j.body, j.created_at, j.deleted_at, j.responsible_id, u.username, u.first_name, u.last_name, 0 AS application_id'
            ' FROM tbl_job j'
            ' INNER JOIN tbl_user u ON j.responsible_id = u.id'
            f'{" WHERE deleted_at IS NULL" if g.user is None or g.user["is_admin"] == False else ""}'
            ' ORDER BY created_at DESC'
        )
    else:
        curs.execute(
            'SELECT j.id, j.title, j.body, j.created_at, j.deleted_at, j.responsible_id, u.username, u.first_name, u.last_name, a.id AS application_id'
            ' FROM tbl_job j'
            ' INNER JOIN tbl_user u ON j.responsible_id = u.id'
            ' LEFT JOIN tbl_application a ON %s = a.applicant_id and j.id = a.job_id'
            f'{" WHERE deleted_at IS NULL" if g.user is None or g.user["is_admin"] == False else ""}'
            ' ORDER BY created_at DESC',
            (g.user["id"],)
        )
    jobs = curs.fetchall()

    curs.close()

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
            flash(error, 'danger')
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'INSERT INTO tbl_job (title, body, responsible_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            conn.commit()

            curs.close()

            flash(f'{ title } has been successfully created.', 'success')
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
            flash(error, 'danger')
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'UPDATE tbl_job SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            conn.commit()

            curs.close()

            flash(f'{ job["title"] } has been successfully updated.', 'success')
            return redirect(url_for('jobs.index'))

    return render_template('jobs/update.html', job=job)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    job = get_job(id)

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('UPDATE tbl_job SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s', (id,))
    conn.commit()

    curs.close()

    flash(f'{ job["title"] } has been successfully deleted.', 'success')
    return redirect(url_for('jobs.index'))

@bp.route('/<int:id>/apply', methods=('GET', 'POST'))
@login_required
def apply(id):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('INSERT INTO tbl_application (applicant_id, job_id) VALUES (%s, %s)', (g.user['id'], id))
    conn.commit()

    curs.close()

    flash('You have successfully applied.', 'success')
    return redirect(url_for('jobs.index'))

@bp.route('/<int:id>/withdraw', methods=('GET', 'POST'))
@login_required
def withdraw(id):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('DELETE FROM tbl_application WHERE applicant_id = %s and job_id = %s', (g.user['id'], id))
    conn.commit()

    curs.close()

    flash('You have successfully withdrawn.', 'success')
    return redirect(url_for('jobs.index'))