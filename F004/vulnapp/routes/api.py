from flask import render_template_string, Blueprint, render_template, jsonify
from vulnapp.database.sql_request import get_blog, get_user

api = Blueprint('api', __name__)


@api.route('/api/<string:function>')
def api_function(function):
    if function == 'blog':
        return api_blog()
    elif function == 'user':
        return api_user()
    return render_template_string(f"API function: {function} not found"), 404

def api_blog():
    blogs = get_blog()
    return jsonify(blogs)

def api_user():
    users = get_user()
    return jsonify(users)
