from flask_jwt_extended import create_access_token

from source.controllers.v1.entities.auth_entity import (AuthDataEntity,
                                                        TokenEntity,
                                                        TokenLinksEntity,
                                                        UserEntity,
                                                        UserLinksEntity)
from source.controllers.v1.entities.link import HttpMethod, LinkEntity
from source.models.user import User, UserData


def to_auth_data(entity: AuthDataEntity) -> UserData:
    return UserData(username=entity["username"], password=entity["password"])


def _build_user_links() -> UserLinksEntity:
    return UserLinksEntity(
        self_link=LinkEntity(href="/v1/auth/register"),
        login=LinkEntity(href="/v1/auth/login", type=HttpMethod.POST),
    )


def to_user_entity(user: User) -> UserEntity:
    return UserEntity(id=user.id, username=user.username, links=_build_user_links())


def _build_token_links() -> TokenLinksEntity:
    return TokenLinksEntity(
        self_link=LinkEntity(href="/v1/auth/login"),
        register=LinkEntity(href="/v1/auth/register", type=HttpMethod.POST),
        get_all_tasks=LinkEntity(href="/v1/tasks/"),
        create_task=LinkEntity(href="/v1/tasks/", type=HttpMethod.POST),
    )


def to_token_entity(user: User) -> TokenEntity:
    token = create_access_token(str(user.id))
    return TokenEntity(token=token, links=_build_token_links())
