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
    """Создание таблиц в БД"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS items (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT, 
                description     TEXT, 
                price           INT, 
                data            TEXT,
                photo           TEXT
        )
        '''
    )

    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS faq (
                about       TEXT 
            )
        '''
    )

    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS qiwi (
                login       TEXT,
                token       TEXT
            )
        '''
    )
    # c.execute(
    #     '''
    #         INSERT INTO faq VALUES('🔘 Информация. Измените её в главном меню')
    #     '''
    # )

    c.execute(
        '''
            CREATE TABLE IF NOT EXISTS buyers (
                users       TEXT,
                iditem      TEXT,
                comment     TEXT,
                amount      TEXT,
                receipt     TEXT,
                randomnum,
                data TEXT
            )
        '''
    )

    conn.commit()


def get_products():
    """Выводит все продукты"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''
            SELECT * FROM items
        '''
    )
    rows = c.fetchall()
    msg = ''
    for row in rows:



get_products()


def add_data(name: str, description: str, price: int, data: str, photo_id: str):
    """Добавление данных о товаре"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''
           INSERT INTO items 
           (name, description, price, data, photo)
           VALUES (?, ?, ?, ?, ?)
        ''', (name, description, price, data, photo_id))
    conn.commit()


def change_faq(about: str):
    """Изменение FAQ"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''
            SELECT * FROM faq
        '''
    )
    while True:
        row = c.fetchone()
        if row == None:
            break
        c.execute(
            '''
                UPDATE faq SET about = ? WHERE about = ?
            ''', (about, row[0])
        )
    conn.commit()


def remove_all_products_db():
    """Удаление всех товаров из БД"""
    conn = get_connection()
    c = conn.cursor()
    all_items = c.execute(
        '''
        SELECT * FROM items
        '''
    ).fetchall()

    count = 0
    for row in all_items:
        c.execute(
            '''
                DELETE FROM items WHERE id = ?
            ''', (row[0],)
        )
        conn.commit()
        count += 1


def get_faq():
    """Получение faq из БД"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''
        SELECT * FROM faq
        '''
    )
    row = c.fetchall()
    for i in row:
        return i[0]
