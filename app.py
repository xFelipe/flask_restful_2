from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'chave super aleatoria'
api = Api(app)
api.app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}

jwt = JWT(app, authenticate, identity)

items = [{'name': 'item1', 'price': 2.55}]

def get_item_by_name(name):
    return next(filter(lambda i: i.get('name') == name, items), None)

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This is a float field and cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = get_item_by_name(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if get_item_by_name(name):
            return {'error': f"The item '{name}' already exists."}, 400
        request_data = Item.parser.parse_args()
        price = float(request_data['price'])
        item = {'name': name, 'price': price}
        items.append(item)
        return {'item': item}, 201

    def delete(self, name):
        item = get_item_by_name(name)
        if not item:
            return {'error': f"Item '{name}' not found"}, 404
        global items
        items = [i for i in items if i != item]
        return {'message': 'Item deleted', 'item': item}

    def put(self, name):
        parser_data = Item.parser.parse_args()
        item = get_item_by_name(name)
        if item:
            item.update(parser_data)
            return item
        else:
            new_item = {'name': name, 'price': parser_data['price']}
            items.append(new_item)
            return new_item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
