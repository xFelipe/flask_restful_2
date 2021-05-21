import sqlite3
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query_result = cursor.execute(
            'select id, username, password from user where username=?',
            (username,)
        )
        row = query_result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query_result = cursor.execute(
            'select id, username, password from user where id=?',
            (_id,)
        )
        row = query_result.fetchone()
        connection.close()
        print(row)
        if row:
            return cls(*row)
