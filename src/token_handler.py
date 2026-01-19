from __future__ import annotations

from typing import Final, TypedDict, cast

from jwt import decode, encode
from pydantic import BaseModel

from src.models.user import User

__all__ = ("TokenHandler", "Token")


class Token(BaseModel):
    sub: str


class TokenDict(TypedDict):
    sub: str


class TokenHandler:
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret: Final[str] = secret
        self.algorithm: Final[str] = algorithm

    def create_access_token(self, user: User) -> str:
        payload = Token(
            sub=user["email"],
        )
        token = encode(dict(payload), self.secret, algorithm=self.algorithm)
        return token

    def validate_token(self, token: str) -> Token:
        decoded = cast(TokenDict, decode(token, self.secret, algorithms=[self.algorithm]))
        return Token(**decoded)

    def decode_token(self, token: str) -> Token:
        return self.validate_token(token)
