import sqlite3
from flask_restful import Resource, reqparse

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

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='Username is a required text field')
        parser.add_argument('password', type=str, required=True,
                            help='Password is a required text field')
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'error': f"Username '{data['username']}' already exists"},\
                   400

        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            query = 'insert into user (username, password) values (?, ?)'
            cursor.execute(query, (data['username'], data['password']))
            conn.commit()
        return {'message': 'sucess'}, 201
