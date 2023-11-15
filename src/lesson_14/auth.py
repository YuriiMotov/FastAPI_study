from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Optional

from fastapi import Depends, status, Security
from fastapi.exceptions import HTTPException
from fastapi.security import (
    OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select

from config import OAUTH2_SECRET as SECRET_KEY
from database import AsyncSession, get_async_session
from .models import OAuth2User
from . import schemas


class Scopes(Enum):
    me: str = "me"
    items: str = "items"


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

scopes = {
    Scopes.me.value: "Read information about the current user.",
    Scopes.items.value: "Read items."
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="oauth2-tests/token",
    scopes=scopes
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(session: AsyncSession, username: str) -> Optional[OAuth2User]:
    st = select(OAuth2User).filter_by(username=username)
    user = await session.scalar(st)
    if user is not None:
        return user
    else:
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> Optional[OAuth2User]:
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Optional[OAuth2User]:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        scopes: list[str] = payload.get("scopes", [])
        token_data = schemas.TokenData(
            username=username,
            scopes=scopes
        )
    except (JWTError, ValidationError):
        raise credentials_exception
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
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def login(
    session: AsyncSession,
    form_data: OAuth2PasswordRequestForm
):
    user = await authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "scopes": form_data.scopes
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def create_user(
    session: AsyncSession,
    user_data: schemas.UserCreate
) -> schemas.UserCreate:
    user = OAuth2User(
        username=user_data.username,
        fullname=user_data.fullname,
        email=user_data.email,
        disabled=user_data.disabled,
        hashed_password=hash_password(user_data.password)
    )
    session.add(user)
    await session.commit()
    return user_data