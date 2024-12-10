from flask import Blueprint, render_template, request
from vulnapp.database.sql_request import get_blog

search = Blueprint('search', __name__)


@search.route('/search')
def search_page():
    search_arg = request.args.get('q', '')
    xss_tag_replace = ['<script>', '</script>']
    search_arg_sanitized = search_arg.lower()
    for xss_tag in xss_tag_replace:
        search_arg_sanitized = search_arg_sanitized.replace(xss_tag, '')
    blogs = get_blog()
    content_search = [blog for blog in blogs if search_arg_sanitized in blog[1].lower()]
    return render_template('search.html', search=search_arg_sanitized, content=content_search)
