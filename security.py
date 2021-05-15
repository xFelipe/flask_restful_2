from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'Felipe', 'asdf')
]
username_mapping = {user.username: user for user in users}
id_mapping = {user.id: user for user in users}


def authenticate(username, password):
    user = username_mapping.get(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    _id = payload['identity']
    return id_mapping.get(_id)
