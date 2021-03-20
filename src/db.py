import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, forse: bool = False):
    c = conn.cursor()

    if forse:
        c.execute('DROP TABLE IF EXISTS items')

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT, 
            description TEXT, 
            price       INT, 
            data        TEXT
        )
        ''')
    if forse:
        c.execute('DROP TABLE IF EXISTS faq')
    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS faq (
                infa    TEXT 
            )
        ''')
    if forse:
        c.execute('DROP TABLE IF EXISTS qiwi')
    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS qiwi (
                login    TEXT,
                token    TEXT
            )
        ''')
    if forse:
        c.execute('DROP TABLE IF EXISTS buyers')
    c.execute(
        '''
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


@ensure_connection
def add_data(conn, name: str, description: str, price: int, data: str):
    c = conn.cursor()
    c.executemany('INSERT INTO items (name, description, price, data) '
                  'VALUES (?, ?, ?, ?)', (name, description, price, data))
    conn.commit()
