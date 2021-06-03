import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

DB_PATH = 'data.db'

items = [{'name': 'item1', 'price': 2.55}]

class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @classmethod
    def get_by_name(cls, name):
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()
            query = 'SELECT name, price from item where name=?'
            query_result = cursor.execute(query, (name,))
            row = query_result.fetchone()
        return {'name': row[0], 'price': row[1]} if row else None

    @classmethod
    def insert(cls, item):
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()
            query = 'insert into item (name, price) values (?, ?)'
            cursor.execute(query, (item['name'], item['price']))

    @classmethod
    def update(cls, item):
        query = 'UPDATE item SET price=? WHERE name=?'
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(query, (item['price'], item['name']))
        return item

    @classmethod
    def get_all(cls):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            query = 'SELECT name, price from item'

            query_result = cursor.execute(query)

        return [{'name': name, 'price': price} for name, price in query_result]


class ItemRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This is a float field and cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = Item.get_by_name(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if Item.get_by_name(name):
            return {'error': f"The item '{name}' already exists."}, 400

        request_data = self.parser.parse_args()
        price = request_data['price']

        item = {'name': name, 'price': price}

        try:
            Item.insert(item)
        except:
            return {'error': 'An error ocourred to inserting the item.'}, 500

        return {'item': {'name': name, 'price': price}}, 201

    def delete(self, name):
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()
            query = 'DELETE FROM item WHERE name=?'
            cursor.execute(query, (name,))

        if cursor.rowcount == 0:
            return {'error': f"Item '{name}' not found"}, 404

        return {'message': f"Item '{name}' deleted"}

    def put(self, name):
        request_data = self.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}

        if Item.get_by_name(name):
            Item.update(item)
            return item
        else:
            Item.insert(item)
            return item, 201


class ItemListRegister(Resource):
    def get(self):
        return Item.get_all()
