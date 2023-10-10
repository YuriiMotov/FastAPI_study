from fastapi import Depends
from fastapi_users.authentication import (
    CookieTransport, AuthenticationBackend, BearerTransport  
) 
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy


from config import SECRET_AUTH_COOKIE
from models.models import AccessToken
from .database import get_access_token_db

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/db/login")

SECRET = SECRET_AUTH_COOKIE

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend_cookie_jwt = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


auth_backend_bearer_db = AuthenticationBackend(
    name="bdb",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)