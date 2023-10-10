from datetime import datetime
from enum import Enum
from typing import Optional, Union

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth.auth import (
    auth_backend_cookie_jwt,
    auth_backend_bearer_db 
)
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate, UserUpdate

app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend_cookie_jwt, auth_backend_bearer_db],
)

# Cookie+jwt authorisation router
app.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie_jwt),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Bearer+db authorisation router
app.include_router(
    fastapi_users.get_auth_router(auth_backend_bearer_db),
    prefix="/auth/bdb",
    tags=["auth"]
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)


# It will generate /forgot-password and /reset-password routes
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth']
)


# It will generate routes to watch and change user's data
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/auth',
    tags=['auth']
)