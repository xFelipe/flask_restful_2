import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

users = [(1, 'Felipe', 'asdf'), (2, 'rolf', 'qwer'), (3, 'anne', 'zxcv')]
insert_query = 'insert into user (id, username, password) values (?, ?, ?)'
cursor.executemany(insert_query, users)
connection.commit()

select_query = 'select * from user'
for line in cursor.execute(select_query):
    print(line)

connection.close()
