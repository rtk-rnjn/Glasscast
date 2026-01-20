from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic.type_adapter import TypeAdapter
from pyowm.weatherapi30.location import Location
from pyowm.weatherapi30.observation import Observation
from pyowm.weatherapi30.weather import Weather
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.app import own_manager, supabase_client, token_handler
from src.models import User
from src.token_handler import Token

router = APIRouter(
    prefix="/data",
    tags=["data"],
)

security = HTTPBearer()
Pydantic_User = TypeAdapter(User)


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> Token:
    token_data = token_handler.decode_token(token.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token_data


@router.get("/search/{city_name}")
async def search_city(
    city_name: str,
    current_user: Token = Depends(get_current_user),
) -> list[tuple[str, int]]:
    search_results = own_manager.weather_at_places(city_name, searchtype="like", limit=10)
    if search_results is None:
        return []

    observations = search_results
    results = []
    for obs in observations:
        assert isinstance(obs, Observation)

        location: Location = obs.location
        results.append([f"{location.name}, {location.country}", int(location.id)])
    return results


@router.get("/weather/{id}")
async def get_weather(
    id: int,
    current_user: Token = Depends(get_current_user),
) -> dict:
    weather_data = own_manager.weather_at_id(id)
    if weather_data is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    weather = weather_data.weather
    return weather.to_dict()


@router.get("/forecast/{id}")
async def get_forecast(
    id: int,
    current_user: Token = Depends(get_current_user),
) -> list[dict]:
    forecast_data = own_manager.forecast_at_id(id, "3h")
    if forecast_data is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    forecast_list: list[Weather] = forecast_data.forecast.weathers
    return [weather.to_dict() for weather in forecast_list]


@router.get("/add_favorite/{id}")
async def add_favorite_city(
    id: int,
    current_user: Token = Depends(get_current_user),
) -> bool:

    supabase_client.from_("cities").insert({"user_email": current_user.sub, "city_id": int(id)}).execute()
    return True


@router.get("/favorites")
async def get_favorite_cities(
    current_user: Token = Depends(get_current_user),
) -> list[int]:
    response = supabase_client.from_("cities").select("city_id").eq("user_email", current_user.sub).execute()
    favorite_cities = response.data

    city_ids: list[int] = [city["city_id"] for city in favorite_cities]
    return list(set(city_ids))
