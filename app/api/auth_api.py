from flask import request, jsonify
from flask_restful import Resource
from app import flask_bcrypt, app

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database.user_db import get_user_details_from_email, create_users

from ..exceptions import UserNotFountException, InvalidUserPayload, UserExistsException

from ..models.user import User

from ..schemas.user_schema import UserSchema

user_schema = UserSchema()

class AuthApi(Resource):
    def post(self):
        app.logger.debug("Debug log level")
        app.logger.info("Program running correctly")
        app.logger.warning("Warning; low disk space!")
        app.logger.error("Error!")
        app.logger.critical("Program halt!")
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        conn = get_db_connection()
        user = get_user_details_from_email(conn, email)
        if user is None:
            raise UserNotFountException(f'User with [{email}] not found in database', 400)

        if email != user.email or not flask_bcrypt.check_password_hash(user.password, password):
            return { "msg": 'Bad email or password'}, 401
        

        additional_claims = {'role': user.role, 'user_id': user.id}

        access_token = create_access_token(identity=email, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=email)
        return {"access_token": access_token, "refresh_token": refresh_token}
    
class RefreshTokernApi(Resource):
    decorators = [jwt_required(refresh=True)]
    def post(self):
        identity = get_jwt_identity()

        conn = get_db_connection()
        user = get_user_details_from_email(conn, identity)
        if user is None:
            raise UserNotFountException(f'User with email [{identity}] not found in database')
        
        additional_claims = {"role": user.role, "user_id": user.id }
        access_token = create_access_token(identity=identity, additional_claims= additional_claims)
        print(get_jwt())
        return {"access_token": access_token}
    

class RegisterApi(Resource):

    def post(self):

        user_payload = request.json
        user_payload['role'] = 'USER'
        #validate incoming data with defined schema for user(validation)
        errors = user_schema.validate(user_payload)
        if errors:
            raise InvalidUserPayload(errors, 400)
        
        #check user exists

        conn = get_db_connection()
        email = user_payload.get('email', None)
        existingUser = get_user_details_from_email(conn, email)
        if existingUser is not None:
            raise UserExistsException(f'User with email id: [{email}] already exists in database')
        
        user = User.from_json(user_payload)
        user.password = flask_bcrypt.generate_password_hash(user.password, 10).decode('utf-8')
        
        new_user = create_users(conn, user)
        commit_and_close_db_connection(conn)

        # print('new user', new_user.to_json())
        return new_user.to_json(), 201


'''
class AuthApi(Resource):
    def post(self):
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if email != 'test@gmail.com' or password != 'test':
            return {'msg' : 'Bad email or password'}, 401
        
        access_token = create_access_token(identity=email)
        return {"access_token" : access_token}
'''

class ProtectedApi(Resource):
    decorators = [jwt_required()]
    def get(self):
        current_user = get_jwt_identity()
        return { 'logged in as': current_user}
    