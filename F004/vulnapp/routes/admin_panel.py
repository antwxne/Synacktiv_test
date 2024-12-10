from flask import Blueprint, render_template, request, flash, make_response
from werkzeug.utils import secure_filename
from vulnapp.database.sql_request import check_login, add_user_cookie
from vulnapp.core.decorators import login_required
from vulnapp.core.forms import UploadForm
from vulnapp.core.config import STATIC_FOLDER
import logging

_logger = logging.getLogger(__name__)
admin_panel = Blueprint('admin_panel', __name__)


@admin_panel.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username and password:
            user_id = check_login(username, password)
            if user_id:
                new_cookie = add_user_cookie(user_id[0])
                response = make_response("success")
                response.set_cookie('SpaceCookie', new_cookie)
                flash('Access granted', 'info')
                return response
        flash('Access denied', 'error')
    return render_template('login.html')


@admin_panel.route('/admin/logout')
@login_required
def logout():
    resp = make_response("del success")
    resp.delete_cookie('SpaceCookie')
    return resp


@admin_panel.route('/admin/panel', methods=['GET'])
@login_required
def panel():
    #uploadform = UploadForm(meta={'csrf': False})
    return render_template('dashboard.html', uploadform="uploadform", message='')

@admin_panel.route('/admin/panel/upload', methods=['GET', 'POST'])
def upload():
    msg = ''
    if request.method == 'POST':
        msg = 'ERROR'
        if 'file' in request.files:
            fdata = request.files['file']
            filename = fdata.filename
            sfilename = secure_filename(filename)
            complete_filepath = STATIC_FOLDER + 'static/img/' + filename
            fdata.save(complete_filepath)
            msg = 'SUCCESS'
    return render_template('admin_upload.html', message=msg)
