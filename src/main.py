from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Security

import auth
from models.oauth2user import OAuth2UserCreate, OAuth2UserOut, OAuth2UserDB
from models.tokens import Tokens
from routers.heroes import heroes_router
from routers.teams import teams_router


app = FastAPI()


oauth2_router = APIRouter()


@oauth2_router.post("/token", response_model=Tokens)
async def login_for_access_token(
    tokens: Annotated[Tokens, Depends(auth.login)],
):
    return tokens


@oauth2_router.post("/register", response_model=OAuth2UserOut)
async def register_user(
    user: Annotated[OAuth2UserCreate, Depends(auth.create_user)]
):
    return user


@oauth2_router.get("/users/me", response_model=OAuth2UserOut)
async def get_users_me(
    current_user: Annotated[
        OAuth2UserDB,
        Security(auth.get_current_active_user, scopes=[auth.Scopes.me.value])
    ]
):
    return current_user

@oauth2_router.get("/items")
async def get_items(
    current_user: Annotated[
        OAuth2UserDB,
        Security(auth.get_current_active_user, scopes=[auth.Scopes.items.value])
    ]
) -> str:
    return "Secret items"


app.include_router(
    oauth2_router,
    prefix="/oauth2-tests",
    tags=["oauth2"]
)

app.include_router(heroes_router)
app.include_router(teams_router)