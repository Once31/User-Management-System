from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app import flask_bcrypt

from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database.user_db import get_users, create_users, get_user_details_from_email, delete_users

from ..models.user import User
from ..schemas.user_schema import UserSchema

from ..exceptions import InvalidUserPayload, UserExistsException

user_schema = UserSchema()

from ..decorators.security import admin_required

class UsersApi(Resource):
    decorators = [jwt_required(), admin_required()]

    def get(self):
        conn = get_db_connection()
        users = get_users(conn)
        close_db_connection(conn)
        return users
    
    def post(self):
        errors = user_schema.validate(request.json)
        print('errors', str(errors))

        if errors:
            raise InvalidUserPayload(errors, 400)
        
        conn = get_db_connection()

        existing_user = get_user_details_from_email(conn, request.json.get('email'))

        if existing_user is not None:
            raise UserExistsException(f"User with email id: [{request.json.get('email')}] already exists", 400)
        
        print('existing_user',existing_user)

        user = User.from_json(request.json)
        user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
        create_users(conn, user)
        users = get_users(conn)
        commit_and_close_db_connection(conn)
        return users, 201


    def delete(self):
        conn= get_db_connection()
        delete_users(conn)

        return {'message': "All users deleted..."}

        