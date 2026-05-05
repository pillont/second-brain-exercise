from flask_jwt_extended import create_access_token

from source.controllers.v1.authent.auth_dto import (
    AuthDataDTO,
    TokenDTO,
    TokenLinksDTO,
    UserDTO,
    UserLinksDTO,
)
from source.controllers.v1.utils.link import HttpMethod, LinkDTO
from source.models.user import User, UserData


def to_auth_data(DTO: AuthDataDTO) -> UserData:
    return UserData(username=DTO["username"], password=DTO["password"])


def _build_user_links() -> UserLinksDTO:
    return UserLinksDTO(
        self_link=LinkDTO(href="/v1/auth/register"),
        login=LinkDTO(href="/v1/auth/login", type=HttpMethod.POST),
    )


def to_user_dto(user: User) -> UserDTO:
    return UserDTO(id=user.id, username=user.username, links=_build_user_links())


def _build_token_links() -> TokenLinksDTO:
    return TokenLinksDTO(
        self_link=LinkDTO(href="/v1/auth/login"),
        register=LinkDTO(href="/v1/auth/register", type=HttpMethod.POST),
        get_all_tasks=LinkDTO(href="/v1/tasks/"),
        create_task=LinkDTO(href="/v1/tasks/", type=HttpMethod.POST),
    )


def to_token_dto(user: User) -> TokenDTO:
    token = create_access_token(str(user.id))
    return TokenDTO(token=token, links=_build_token_links())
