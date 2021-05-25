import sqlite3

with sqlite3.connect('data.db') as conn:
    user_query = 'CREATE TABLE user '\
                 '(id INTEGER PRIMARY KEY, username text, password text)'
    item_query = 'CREATE TABLE item ' \
                 '(id INTEGER PRIMARY KEY, name TEXT, price REAL)'
    insert_item = 'INSERT INTO item (name, price) VALUES ("itemz", 10.99)'
    cursor = conn.cursor()
    cursor.execute(user_query)
    cursor.execute(item_query)
    cursor.execute(insert_item)
