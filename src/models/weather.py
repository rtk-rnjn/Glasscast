from __future__ import annotations

from typing import Dict, Optional, TypedDict


class Wind(TypedDict):
    speed: float
    deg: int
    gust: float


class Pressure(TypedDict):
    press: int
    sea_level: int


class Temperature(TypedDict):
    temp: float
    temp_kf: Optional[float]
    temp_max: float
    temp_min: float
    feels_like: float


class WeatherData(TypedDict):
    reference_time: int
    sunset_time: int
    sunrise_time: int
    clouds: int
    rain: Dict[str, float]
    snow: Dict[str, float]
    wind: Wind
    humidity: int
    pressure: Pressure
    temperature: Temperature
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    visibility_distance: int
    dewpoint: Optional[float]
    humidex: Optional[float]
    heat_index: Optional[float]
    utc_offset: int
    uvi: Optional[float]
    precipitation_probability: Optional[float]
