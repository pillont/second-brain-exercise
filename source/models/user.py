from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    password: str


@dataclass
class User:
    id: int
    username: str
    hashed_password: str
