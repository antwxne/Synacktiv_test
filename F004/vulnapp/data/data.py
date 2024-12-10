from vulnapp.database.db import db, session
from vulnapp.database.sql_request import get_blog


def add_data():

    blog = get_blog(1)

    if not blog:
        session.execute(
            '''INSERT INTO blog (title, content, date) VALUES('LOREM IPSUM', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '11-10-2021');''')
        session.execute(
            '''INSERT INTO user (username, password, cookie) VALUES('admin', 'admin', NULL), ('SpaceUnion', 'Sp@ce0ign0n', NULL), ('JandBezor', 'M@M@Z0N', NULL);''')
        db.commit()
