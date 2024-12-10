from flask import render_template_string, Blueprint, render_template, request
from vulnapp.database.sql_request import get_blog, sql_filter

blog = Blueprint('blog', __name__)


@blog.route('/blog')
def blog_page():
    blog_id = request.args.get('id', '')
    blogposts = []
    mode = 'all'
    if blog_id and sql_filter(blog_id):
        result = get_blog(blog_id)
        if result:
            blogposts = result
            mode = 'view'
    else:
        blogposts = get_blog()
    return render_template('blog.html', blogposts=blogposts, mode=mode)
