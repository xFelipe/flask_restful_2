from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import ItemRegister, ItemListRegister

app = Flask(__name__)
app.secret_key = 'chave super aleatoria'
app.config['JWT_EXPIRATION_DELTA'] = 3600
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemRegister, '/item/<string:name>')
api.add_resource(ItemListRegister, '/items')
api.add_resource(UserRegister, '/register')
