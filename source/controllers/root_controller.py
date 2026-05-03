import logging

from flask_smorest import Blueprint

from source.controllers.entities.entry_point_entity import EntryPointEntity
from source.controllers.mappers.entry_point_mapper import to_entry_point_entity
from source.controllers.schemas.entry_point_schema import EntryPointSchema

logger = logging.getLogger(__name__)

root_blp = Blueprint("root", __name__, url_prefix="")


@root_blp.route("/", methods=["GET"])
@root_blp.doc(summary="Entry point", description="Returns the API root links.")
@root_blp.response(200, EntryPointSchema)
def get_entry_point() -> EntryPointEntity:
    return to_entry_point_entity()
