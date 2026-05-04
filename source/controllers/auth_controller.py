from dependency_injector.wiring import Provide, inject
from flask import abort
from flask_smorest import Blueprint

from source.container import Container
from source.controllers.entities.auth_entity import (
    AuthDataEntity,
    TokenEntity,
    UserEntity,
)
from source.controllers.mappers.auth_mapper import (
    to_auth_data,
    to_token_entity,
    to_user_entity,
)
from source.controllers.schemas.auth_data_schema import AuthDataSchema
from source.controllers.schemas.token_schema import TokenSchema
from source.controllers.schemas.user_schema import UserSchema
from source.models.invalid_credentials_error import InvalidCredentialsError
from source.models.user_already_exists_error import UserAlreadyExistsError
from source.services.login_user_service import LoginUserService
from source.services.register_user_service import RegisterUserService

auth_blp = Blueprint(
    "auth", __name__, url_prefix="/auth", description="Authentication endpoints."
)


@auth_blp.route("/register", methods=["POST"])
@auth_blp.doc(summary="Register", description="Create a new user account.")
@auth_blp.arguments(AuthDataSchema)
@auth_blp.response(409)
@auth_blp.response(201, UserSchema)
@inject
def register(
    auth_data_entity: AuthDataEntity,
    register_user_service: RegisterUserService = Provide[
        Container.register_user_service
    ],
) -> UserEntity:
    user_data = to_auth_data(auth_data_entity)
    try:
        user = register_user_service.register_user(user_data)
    except UserAlreadyExistsError:
        abort(409)

    return to_user_entity(user)


@auth_blp.route("/login", methods=["POST"])
@auth_blp.doc(
    summary="Login", description="Authenticate and receive a JWT access token."
)
@auth_blp.arguments(AuthDataSchema)
@auth_blp.response(401)
@auth_blp.response(200, TokenSchema)
@inject
def login(
    auth_data_entity: AuthDataEntity,
    login_user_service: LoginUserService = Provide[Container.login_user_service],
) -> TokenEntity:
    try:
        user = login_user_service.login(
            auth_data_entity["username"],
            auth_data_entity["password"],
        )

        return to_token_entity(user)
    except InvalidCredentialsError:
        abort(401)
