from flask import request
from flask_restful import Resource

from flask_jwt_extended import jwt_required

from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database.address_db import get_address, update_address, delete_address

from ..exceptions import InvalidAddressPayload
from ..schemas.address_schema import AddressSchema

from ..models.address import Address

address_schema = AddressSchema()

class AddressApi(Resource):
    decorators = [jwt_required()]
    def get(self, id):
        conn = get_db_connection()
        result = get_address(conn, id)
        close_db_connection(conn)
        return result

    def put(self, id):
        conn = get_db_connection()
        get_address(conn, id)

        errors = address_schema.validate(request.json)
        if errors:
            raise InvalidAddressPayload(errors, 400)

      
        update_address(conn, id, Address.from_json(request.json)) 
        address = get_address(conn, id)
        commit_and_close_db_connection(conn)
        return address   

    def delete(self, id):
        conn = get_db_connection()
        get_address(conn, id)
        delete_address(conn, id)
        commit_and_close_db_connection(conn)
        return {'message': f'Address [{id}] deleted from the database'}
