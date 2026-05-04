from marshmallow import Schema, fields


class ListArgumentSchema(Schema):
    cursor = fields.String(required=False)
    page_size = fields.Integer(required=False)
