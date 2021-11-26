from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort
from reclutamiento.auth import login_required
from reclutamiento.db import get_conn, get_curs
from reclutamiento.profile import get_profile

def get_education(id, check_owner=True):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT e.id, applicant_id, start_date, end_date, institution_name, education_type_id, et.name, education_name'
        ' FROM tbl_education e'
        ' INNER JOIN tbl_education_type et ON e.education_type_id = et.id'
        ' WHERE e.id = %s',
        (id,)
    )
    education = curs.fetchone()

    curs.close()

    if education is None:
        abort(404, f"Education id {id} doesn't exist.")

    if check_owner and education['applicant_id'] != g.user['id']:
        abort(403)

    return education

bp = Blueprint('education', __name__)

@bp.route('/<int:profile_id>/education/add', methods=('GET', 'POST'))
@login_required
def add(profile_id):
    profile = get_profile(profile_id)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        education_type = request.form['education_type']
        institution_name = request.form['institution_name']
        education_name = request.form['education_name']
        error = None

        if not start_date:
            error = 'Start date is required.'

        if not end_date:
            error = 'End date is required.'

        if not datetime.strptime(start_date, '%Y-%m-%d') < datetime.strptime(end_date, '%Y-%m-%d'):
            error = 'End date should be greater than start date.'

        if not education_type:
            error = 'Education type is required.'

        if not institution_name:
            error = 'Institution name is required.'

        if not education_name:
            error = 'Education name is required.'

        if error is not None:
            flash(error, 'danger')
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'INSERT INTO tbl_education (applicant_id, start_date, end_date, institution_name, education_type_id, education_name)'
                ' VALUES (%s, %s, %s, %s, %s, %s)',
                (profile_id, start_date, end_date, institution_name, education_type, education_name)
            )
            conn.commit()

            curs.close()

            flash('Education has been successfully created.', 'success')
            return redirect(url_for('profile.index', id=profile_id))

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT id, name'
        ' FROM tbl_education_type'
    )
    education_types = curs.fetchall()

    curs.close()

    return render_template('education/add.html', education_types=education_types)

@bp.route('/<int:profile_id>/education/remove/<int:education_id>', methods=('GET', 'POST'))
@login_required
def remove(profile_id, education_id):
    education = get_education(education_id)

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute('DELETE FROM tbl_education WHERE id = %s', (education_id,))
    conn.commit()

    curs.close()

    flash('Education has been successfully removed.', 'success')
    return redirect(url_for('profile.index', id=profile_id))