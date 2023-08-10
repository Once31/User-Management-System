
from flask import request
from flask_restful import Resource

from flask_jwt_extended import jwt_required

from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database.address_db import get_addresses, create_address

from ..schemas.address_schema import AddressSchema

from ..exceptions import InvalidAddressPayload

from ..models.address import Address

address_schema = AddressSchema()

from ..decorators.security import admin_or_self_required

class AddressesApi(Resource):
    decorators = [jwt_required(), admin_or_self_required(user_id_param='user_id')]
    def get(self, user_id):
        conn = get_db_connection()
        results = get_addresses(conn, user_id)
        close_db_connection(conn)
        return results

    def post(self, user_id):
        errors = address_schema.validate(request.json)
        if errors:
            raise InvalidAddressPayload(errors, 400)
        
        conn = get_db_connection()
        create_address(conn, Address.from_json(request.json), user_id)
        addresses = get_addresses(conn, user_id)
        commit_and_close_db_connection(conn)
        return addresses, 201


    def put(self):
        pass

    def delete(self):
        pass
