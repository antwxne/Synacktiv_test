from functools import wraps
from flask import g, request, redirect, url_for
from vulnapp.database.sql_request import get_user_cookie


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        spacecookie = request.cookies.get('SpaceCookie')
        if not spacecookie or not get_user_cookie(spacecookie):
            return redirect(url_for('admin_panel.login', next=request.url)), 302
        return f(*args, **kwargs)
    return decorated_function
