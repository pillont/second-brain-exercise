from marshmallow import Schema, fields


class LinkSchema(Schema):
    href = fields.Str(required=True)


class LinksSchema(Schema):
    self_link = fields.Nested(LinkSchema, data_key="self", required=True)
