from vulnapp.database.db import db, session
from uuid import uuid4
from logging import getLogger

_logger = getLogger(__name__)

def get_blog(blog_id=None):
    opt_param = ''
    if blog_id:
        opt_param = f'where id={blog_id}'
    request = f'select * from blog {opt_param};'
    result = session.execute(request)
    if result:
        res_list = [res for res in result]
        return res_list
    return False


def add_blog(title, content):
    request = f"insert into blog (title, content) values('{title}', '{content}');"
    session.execute(request)
    db.commit()


def get_user(user_id=None):
    opt_param = ''
    if user_id:
        opt_param = f'where id={user_id}'
    request = f'select * from user {opt_param};'
    result = session.execute(request)
    if result:
        res_list = [res for res in result]
        return res_list
    return False


def add_user(username, password):
    pass


def add_user_cookie(user_id):
    cookie_value = str(uuid4())
    request = f"update user set cookie='{cookie_value}' where id={user_id};"
    session.execute(request)
    db.commit()
    return cookie_value


def get_user_cookie(cookie):
    _logger.warning('Cookie value:' + str(cookie))
    request = f"select id from user where cookie='{cookie}';"
    result = session.execute(request)
    result_list = [res for res in result]
    if result_list:
        return result_list[0]
    return 0


def check_login(username, password):
    request = f"select id from user where username='{username}' and password='{password}';"
    result = session.execute(request)
    result_list = [res for res in result]
    if result_list:
        return result_list[0]
    return 0


def sql_filter(user_input):
    blacklist = ['union', 'or']
    user_input_lower = user_input.lower()
    has_black_word = list(filter(lambda bw: bw in user_input_lower, blacklist))
    return len(has_black_word) == 0
