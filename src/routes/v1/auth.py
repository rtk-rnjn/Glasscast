from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.app import supabase_client, token_handler
from src.models import UserModel
from src.token_handler import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> Token:
    token_data = token_handler.decode_token(token.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token_data


def check_user_exists(email: str) -> bool:
    response = supabase_client.from_("users").select("*").eq("email", email).execute()
    return len(response.data) > 0


def create_user(*, email: str, password: str):
    user_data = {"email": email, "password": password}
    supabase_client.from_("users").insert(user_data).execute()


def get_user_by_email(email: str) -> UserModel | None:
    response = supabase_client.from_("users").select("*").eq("email", email).execute()
    if len(response.data) == 0:
        return None

    email_str: str = response.data[0]["email"]
    password: str = response.data[0]["password"]

    return UserModel(email=email_str, password=password)


@router.get("/me")
async def read_current_user(current_user: Token = Depends(get_current_user)) -> Token:
    return current_user


@router.post("/create")
async def create_user_endpoint(user: UserModel):
    if check_user_exists(user.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    create_user(email=user.email, password=user.password)
    access_token = token_handler.create_access_token({"email": user.email, "password": user.password})
    return {"access_token": access_token}


@router.post("/login")
async def login_user(user: UserModel):
    if not check_user_exists(user.email):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    supabase_user = get_user_by_email(user.email)
    if supabase_user is None or supabase_user.password != user.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = token_handler.create_access_token({"email": user.email, "password": user.password})
    return {"access_token": access_token}
