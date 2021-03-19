import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn):
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT, 
            description TEXT, 
            price       INT, 
            data        TEXT
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                infa    TEXT 
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS qiwi (
                login    TEXT,
                token    TEXT
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS buyers (
                users    TEXT,
                iditem   TEXT,
                comment  TEXT,
                amount   TEXT,
                receipt  TEXT,
                randomnum,
                data TEXT
            )
        ''')

    conn.commit()



