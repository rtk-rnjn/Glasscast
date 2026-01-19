from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel


class User(TypedDict):
    email: str
    password: str


class FavoriteCity(TypedDict):
    user_email: str
    city_id: str


class UserModel(BaseModel):
    email: str
    password: str


class FavoriteCityModel(BaseModel):
    user_email: str
    city_id: str
