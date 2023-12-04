from enum import Enum
from typing import Annotated, Optional

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes)
from passlib.context import CryptContext
from sqlalchemy import select

from config import OAUTH2_SECRET as SECRET_KEY
from database import AsyncSession, get_async_session
from oauth_password_refresh_scheme import OAuth2PasswordAndRefreshRequestForm
from models.oauth2user import OAuth2UserCreate, OAuth2UserDB
from models.tokens import Tokens
from token_service import TokenService, TokenServiceDep, MemoryStorage


class Scopes(Enum):
    me: str = "me"
    items: str = "items"

token_service_dep = TokenServiceDep(
    secret=SECRET_KEY,
    storage_class=MemoryStorage,
)

app_scopes = {
    Scopes.me.value: "Read information about the current user.",
    Scopes.items.value: "Read items."
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="oauth2-tests/token",
    scopes=app_scopes
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(session: AsyncSession, username: str) -> Optional[OAuth2UserDB]:
    st = select(OAuth2UserDB).filter_by(username=username)
    user = await session.scalar(st)
    if user is not None:
        return user
    else:
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user_pwd_or_refreshtoken(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    form_data: Annotated[OAuth2PasswordAndRefreshRequestForm, Depends()],
    token_service: Annotated[TokenService, Depends(token_service_dep)]
) -> OAuth2UserDB:
    user = None
    if form_data.grant_type == "password":
        user = await get_user(session, form_data.username)
        if user and (not verify_password(form_data.password, user.hashed_password)):
            user = None
    elif form_data.grant_type == "refresh_token":
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if not form_data.refresh_token:
            raise credentials_exception
        refresh_token_data = await token_service.validate_refresh_token(
            token=form_data.refresh_token,
            credentials_exception=credentials_exception
        )
        user = await get_user(session, refresh_token_data.username)
        for scope in form_data.scopes:
            if scope not in refresh_token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The requested scope is not allowed for this user"
                )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return  user


async def get_current_user(
    security_scopes: SecurityScopes,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(token_service_dep)]
) -> Optional[OAuth2UserDB]:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    token_data = await token_service.validate_access_token(
        token=token,
        credentials_exception=credentials_exception
    )
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[OAuth2UserDB, Depends(get_current_user)]
) -> OAuth2UserDB:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def login(
    form_data: Annotated[OAuth2PasswordAndRefreshRequestForm, Depends()],
    token_service: Annotated[TokenService, Depends(token_service_dep)],
    user: Annotated[OAuth2UserDB, Depends(authenticate_user_pwd_or_refreshtoken)]
) -> Tokens:
    user_scopes = user.scopes.split(' ')
    scopes = []
    for scope in form_data.scopes:
        if scope in user_scopes:
            scopes.append(scope)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The requested scope is not allowed for this user"
            )

    token_data = {"sub": user.username, "scopes": scopes}
    access_token = await token_service.create_access_token(data=token_data)
    refresh_token = await token_service.create_refresh_token(data=token_data)

    return Tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: OAuth2UserCreate
) -> OAuth2UserDB:
    user = OAuth2UserDB(
        **user_data.model_dump(exclude=["password"]),
        hashed_password=hash_password(user_data.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user