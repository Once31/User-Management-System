from flask import request
from flask_restful import Resource
from app import flask_bcrypt
from flask_jwt_extended import jwt_required

from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database.user_db import get_user, update_user , delete_user

from ..exceptions import InvalidUserPayload, UserNotFountException

from ..schemas.user_schema import UserSchema

from ..models.user import User

from ..decorators.security import admin_or_self_required

user_schema = UserSchema()

class UserApi(Resource):
    decorators = [jwt_required(), admin_or_self_required()]
    def get(self, id):
        print('id',id)
        conn = get_db_connection()
        result = get_user(conn, id)
        commit_and_close_db_connection(conn)
        return result

    def put(self, id):
        conn = get_db_connection()
        get_user(conn, id)

        errors = user_schema.validate(request.json)
        if errors: 
            raise InvalidUserPayload(errors, 400)

        print(request.json)        
        user = User.from_json(request.json)
        user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
        update_user(conn, id, user)
        user = get_user(conn, id)
        commit_and_close_db_connection(conn)
        return user

    def delete(self, id):
        conn = get_db_connection()
        user = get_user(conn, id)
        if user is None: 
            raise UserNotFountException("User not exists", 400)
        delete_user(conn, id)
        commit_and_close_db_connection(conn)
        return {'message': f'User [{user["name"]}] deleted from DATABASE'}
