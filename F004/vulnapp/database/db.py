import sqlite3

db = sqlite3.connect('spacey.db', check_same_thread=False)
session = db.cursor()


def init_table():
    session.execute(
        '''CREATE TABLE IF NOT EXISTS blog (id integer primary key autoincrement, title text not null, content text not null, date text)''')
    session.execute(
        '''CREATE TABLE IF NOT EXISTS user (id integer primary key autoincrement, username text not null, password text not null, cookie text)''')
    db.commit()
