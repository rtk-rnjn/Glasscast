from fastapi import APIRouter

from .auth import router as auth_router
from .weather import router as weather_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(auth_router)
router.include_router(weather_router)
