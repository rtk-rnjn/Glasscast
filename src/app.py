from __future__ import annotations

import os

import supabase
from dotenv import load_dotenv
from fastapi import FastAPI
from pyowm import OWM

from .token_handler import TokenHandler

load_dotenv()


owm = OWM(os.environ["OWM_API_KEY"])
own_manager = owm.weather_manager()
token_handler = TokenHandler(secret=os.getenv("JWT_SECRET", "JWT_SECRET"))
supabase_client = supabase.Client(
    supabase_url=os.environ["SUPABASE_URL"],
    supabase_key=os.environ["SUPABASE_KEY"],
)

app = FastAPI(
    title="Glasscast - Weather Forecasting Service",
    description="A service that provides accurate and up-to-date weather forecasts.",
    version="1.0.0",
)

app.state.own_manager = own_manager

from .routes import v1_router  # noqa

app.include_router(v1_router)
