import sqlite3


# def ensure_connection(func):
#     """ Декоратор для подключения к СУБД: открывает соединение,
#         выполняет переданную функцию и закрывает за собой соединение.
#         Потокобезопасно!
#     """
#
#     def inner(*args, **kwargs):
#         with sqlite3.connect('database.db') as conn:
#             res = func(*args, conn=conn, **kwargs)
#         return res
#
#     return inner

_connection = None


def get_connection():
    """Подключение к БД"""
    global _connection
    if _connection is None:
        _connection = sqlite3.connect('database.db')
    return _connection


def init_db():
    """Создание таблици в БД"""
    conn = get_connection()
    c = conn.cursor()
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

    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS faq (
                infa    TEXT 
            )
        ''')

    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS qiwi (
                login    TEXT,
                token    TEXT
            )
        ''')

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


def add_data(name: str, description: str, price: int, data: str):
    """Добавление данных о товаре"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO items 
           (name, description, price, data)
           VALUES (?, ?, ?, ?)
        ''', (name, description, price, data))
    conn.commit()
