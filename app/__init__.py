from flask import Flask
from flask_restful import Api
from .config import load_configuration

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from .models.user import User
from .utils import create_admin

import logging
from flask.logging import default_handler 

app = Flask(__name__)
load_configuration(app)
# print('config',app.config)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code':e.code, 'message': 'error', 'errors': e.message}, e.code
restful_api = CustomApi(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)


with app.app_context():
    print('before first request')
    admin = User.from_json({
        "name": "Admin",
        "email": app.config['UMS_ADMIN_EMAIL'],
        "password": app.config['UMS_ADMIN_PASSWORD'],
        "role": 'ADMIN',
        'age': 23
    })
    print(app.config['DATABASE_URI'])
    create_admin(flask_bcrypt, admin)


# @app.got_first_request
# def before_first_request():
#     print('before first request')
#     return 'hello'


## logging settings
app.logger.setLevel(logging.INFO)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s %(threadName)s: %(message)s]'
))

# app.logger.addHandler(default_handler)
app.logger.info('hello guys')

# app.logger.info('hello guys')