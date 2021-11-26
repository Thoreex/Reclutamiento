from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort
from reclutamiento.auth import login_required
from reclutamiento.db import get_conn, get_curs
from reclutamiento.profile import get_profile

def get_experience(id, check_owner=True):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT id, applicant_id, start_date, end_date, company_name, job_title, job_description'
        ' FROM tbl_experience e'
        ' WHERE e.id = %s',
        (id,)
    )
    experience = curs.fetchone()

    curs.close()

    if experience is None:
        abort(404, f"Experience id {id} doesn't exist.")

    if check_owner and experience['applicant_id'] != g.user['id']:
        abort(403)

    return experience

bp = Blueprint('experience', __name__)

@bp.route('/<int:profile_id>/experience/add', methods=('GET', 'POST'))
@login_required
def add(profile_id):
    profile = get_profile(profile_id)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        error = None

        if not start_date:
            error = 'Start date is required.'

        if not end_date:
            error = 'End date is required.'

        if not datetime.strptime(start_date, '%Y-%m-%d') < datetime.strptime(end_date, '%Y-%m-%d'):
            error = 'End date should be greater than start date.'

        if not company_name:
            error = 'Company name is required.'

        if not job_title:
            error = 'Job title is required.'

        if not job_description:
            error = 'Job description is required.'

        if error is not None:
            flash(error, 'danger')
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'INSERT INTO tbl_experience (applicant_id, start_date, end_date, company_name, job_title, job_description)'
                ' VALUES (%s, %s, %s, %s, %s, %s)',
                (profile_id, start_date, end_date, company_name, job_title, job_description)
            )
            conn.commit()

            curs.close()

            flash('Experience has been successfully created.', 'success')
            return redirect(url_for('profile.index', id=profile_id))

    return render_template('experience/add.html')

@bp.route('/<int:profile_id>/experience/remove/<int:experience_id>', methods=('GET', 'POST'))
@login_required
def remove(profile_id, experience_id):
    experience = get_experience(experience_id)

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('DELETE FROM tbl_experience WHERE id = %s', (experience_id,))
    conn.commit()

    curs.close()

    flash('Experience has been successfully removed.', 'success')
    return redirect(url_for('profile.index', id=profile_id))