from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from reclutamiento.auth import login_required
from reclutamiento.db import get_conn, get_curs

def get_profile(id, check_owner=True):
    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT id, username, password, first_name, last_name, email, phone_number, is_admin'
        ' FROM tbl_user'
        ' WHERE id = %s',
        (id,)
    )
    profile = curs.fetchone()

    if profile is None:
        abort(404, f"Profile id {id} doesn't exist.")

    if check_owner and profile['id'] != g.user['id']:
        abort(403)

    return profile

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:id>')
def index(id):
    profile = get_profile(id, False)

    conn = get_conn()
    curs = get_curs(conn)

    curs.execute(
        'SELECT e.id, applicant_id, start_date, end_date, institution_name, education_type_id, et.name, education_name'
        ' FROM tbl_education e'
        ' INNER JOIN tbl_education_type et ON e.education_type_id = et.id'
    )
    educations = curs.fetchall()

    curs.execute(
        'SELECT id, applicant_id, start_date, end_date, company_name, job_title, job_description'
        ' FROM tbl_experience e'
    )
    experiences = curs.fetchall()

    return render_template('profile/index.html', profile=profile, educations=educations, experiences=experiences)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    profile = get_profile(id)

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        error = None

        if not first_name:
            error = 'First name is required.'

        if not last_name:
            error = 'Last name is required.'

        if not email:
            error = 'Email is required.'

        if not phone_number:
            error = 'Phone number is required.'

        if error is not None:
            flash(error, 'danger')
        else:
            conn = get_conn()
            curs = get_curs(conn)

            curs.execute(
                'UPDATE tbl_user SET first_name = %s, last_name = %s, email = %s, phone_number = %s'
                ' WHERE id = %s',
                (first_name, last_name, email, phone_number, id)
            )
            conn.commit()

            flash(f'Profile has been successfully updated.', 'success')
            return redirect(url_for('profile.index', id=profile['id']))

    return render_template('profile/update.html', profile=profile)