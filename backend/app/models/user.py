from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class User:
    id: int
    username: str
    hashed_password: str


class UserPublic(BaseModel):
    id: int
    username: str
