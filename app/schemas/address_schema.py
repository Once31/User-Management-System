from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class AddressSchema(Schema):
    id = fields.Int()
    address_line_1 = fields.Str(required=True, validate=Length(max=50))
    city = fields.Str(required=True)
    state = fields.Str(required=True, validate=OneOf( choices= ['MH','UP','GJ','MP','GA','KA','TG','AS','DL','RJ','KL']))
    pin = fields.Int(required=True)