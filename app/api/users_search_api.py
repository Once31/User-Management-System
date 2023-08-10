from flask import request
from flask_restful import Resource

from flask_jwt_extended import jwt_required

from ..models.user import User


class UsersSearchApi(Resource):
    decorators = [jwt_required()]
    def get(self):
        # email = request.args.get('email')
        # if not email:
        #     return {'message': "Mandatory parameter email not found in request"}
        
        # user = User.query
        # return email
        return 'search user'

