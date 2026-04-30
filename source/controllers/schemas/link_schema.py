from typing import Any

from marshmallow import Schema, fields, post_dump

from source.controllers.entities.link import LinkEntity
from source.controllers.entities.task_entity import TaskEntity


class LinkSchema(Schema):
    href = fields.Str(required=True)
    type = fields.Str(required=False, allow_none=False)

    @post_dump
    def remove_none(self, data: LinkEntity, **kwargs) -> Any:
        if data.get("type") is None:
            data.pop("type", None)
        return data


class LinksSchema(Schema):
    self_link = fields.Nested(LinkSchema, data_key="self", required=True)
