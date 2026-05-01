from marshmallow import Schema, fields


class ListArgumentSchema(Schema):
    page_size = fields.Integer(required=False)
    cursor = fields.Integer(required=False)
