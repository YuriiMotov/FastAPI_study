from fastapi import APIRouter
from fastapi_users import fastapi_users, FastAPIUsers

from auth.base_config import (
    auth_backend_cookie_jwt,
    auth_backend_bearer_db 
)
from auth.models import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate, UserUpdate


router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend_cookie_jwt, auth_backend_bearer_db],
)

# Cookie+jwt authorisation router
router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie_jwt),
    prefix="/jwt",
)

# Bearer+db authorisation router
router.include_router(
    fastapi_users.get_auth_router(auth_backend_bearer_db),
    prefix="/bdb",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)

# It will generate /forgot-password and /reset-password routes
router.include_router(
    fastapi_users.get_reset_password_router()
)

# It will generate routes to watch and change user's data
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate)
)