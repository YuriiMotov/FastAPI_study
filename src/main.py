from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Security

import auth
import schemas

app = FastAPI()


oauth2_router = APIRouter()


@oauth2_router.post("/token", response_model=schemas.Tokens)
async def login_for_access_token(
    tokens: Annotated[schemas.Tokens, Depends(auth.login)],
):
    return tokens


@oauth2_router.post("/register", response_model=schemas.User)
async def register_user(
    user: Annotated[schemas.UserCreate, Depends(auth.create_user)]
):
    return user


@oauth2_router.get("/users/me", response_model=schemas.User)
async def get_users_me(
    current_user: Annotated[
        schemas.User,
        Security(auth.get_current_active_user, scopes=[auth.Scopes.me.value])
    ]
):
    return current_user

@oauth2_router.get("/items")
async def get_items(
    current_user: Annotated[
        schemas.User,
        Security(auth.get_current_active_user, scopes=[auth.Scopes.items.value])
    ]
) -> str:
    return "Secret items"


app.include_router(
    oauth2_router,
    prefix="/oauth2-tests",
    tags=["oauth2"]
)

