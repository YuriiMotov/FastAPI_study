from typing import Optional

from sqlmodel import SQLModel, Field


class BaseOAuth2User(SQLModel):
    username: str = Field(max_length=30, nullable=False)
    fullname: str = Field(max_length=60, nullable=False)
    email: str = Field(max_length=320, nullable=False, unique=True, index=True)
    disabled: bool = Field(default=True, nullable=False)
    scopes: str = Field(nullable=True, default='')


class OAuth2UserCreate(BaseOAuth2User):
    password: str = Field(max_length=1024, nullable=False)


class OAuth2UserOut(BaseOAuth2User):
    id: int


class OAuth2UserDB(BaseOAuth2User, table=True):
    __tablename__ = "oauth2_user"
    id: Optional[int] = Field(primary_key=True)
    hashed_password: str = Field(max_length=1024, nullable=False)
    