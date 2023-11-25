from abc import ABC, abstractmethod
from calendar import timegm
from datetime import datetime, timedelta
from typing import Any, Optional, Type

from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import ValidationError

from .schemas import TokenData


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT = 2
REFRESH_TOKEN_EXPIRE_MINUTES_DEFAULT = 60*24


class InvalidToken(Exception):
    pass


class StorageInterface(ABC):

    def __init__(self, expire_minutes: int, **kwargs):
        class_name = self.__class__.__name__
        for param in kwargs.keys():
            print(f"Unknown config paramater in {class_name}.__init__(): {param}")


    @abstractmethod
    async def get_last_exp_dt_timestamp(self, user_name: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def put_last_exp_dt(self, user_name: str, exp_dt_timestamp: int):
        raise NotImplementedError()


class TokenService():

    def __init__(
        self, secret: str,
        storage_class: Type[StorageInterface],
        storage_config: Optional[dict[str, Any]],
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
    ):
        self.secret = secret
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        if storage_config is None:
            storage_config = {}
        self.storage = storage_class(
            expire_minutes=refresh_token_expire_minutes,
            **storage_config
        )
    
    async def create_refresh_token(self, data: dict):
        (token, token_data) = self._create_token(
            data=data,
            is_refresh_token=True,
            token_expire_minutes=self.refresh_token_expire_minutes
        )
        await self.storage.put_last_exp_dt(
            token_data["sub"], token_data["exp"]
        )
        return token

    async def create_access_token(self, data: dict):
        (token, _) = self._create_token(
            data=data,
            is_refresh_token=False,
            token_expire_minutes=self.access_token_expire_minutes
        )
        return token

    async def validate_refresh_token(self, token: str, credentials_exception: HTTPException):
        token_data = self._validate_token(
            token=token,
            is_refresh_token=True,
            credentials_exception=credentials_exception
        )
        await self._check_refresh_token_invalid(
            user_name=token_data.username,
            token_exp_dt_timestamp=token_data.exp
        )
        return token_data


    async def validate_access_token(self, token: str, credentials_exception: HTTPException):
        return self._validate_token(
            token=token,
            is_refresh_token=False,
            credentials_exception=credentials_exception
        )
    
    def _create_token(
        self,
        data: dict,
        is_refresh_token: bool,
        token_expire_minutes: int
    ) -> (str, dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(token_expire_minutes)
        to_encode.update({"exp": expire, "is_refresh_token": is_refresh_token})
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=ALGORITHM)
        return (encoded_jwt, to_encode)
    
    def _validate_token(
        self,
        token: str,
        is_refresh_token: bool,
        credentials_exception: HTTPException
    ) -> TokenData:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            if exp is None:
                raise credentials_exception
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            scopes: list[str] = payload.get("scopes", [])
            if is_refresh_token != payload.get("is_refresh_token", False):
                raise credentials_exception
            token_data = TokenData(
                username=username,
                scopes=scopes,
                exp=exp
            )
        except (JWTError, ValidationError):
            raise credentials_exception
        return token_data

    async def _check_refresh_token_invalid(
        self, user_name: str, token_exp_dt_timestamp: int
    ) -> None:
        last_exp_dt = await self.storage.get_last_exp_dt_timestamp(user_name)
        if (token_exp_dt_timestamp < last_exp_dt):
            await self.storage.unset_last_exp_dt_timestamp(user_name)
            raise InvalidToken()


class MemoryStorage(StorageInterface):
    def __init__(self, expire_minutes: int, **kwargs):
        super().__init__(expire_minutes=expire_minutes, **kwargs)
        self.data: dict[str, int] = {}
        self.expire_minutes = expire_minutes


    async def unset_last_exp_dt_timestamp(self, user_name: str) -> None:
        if user_name in self.data:
            self.data.pop(user_name)

    async def get_last_exp_dt_timestamp(self, user_name: str) -> int:
        return self.data.get(
            user_name,
            timegm((datetime.utcnow() + timedelta(self.expire_minutes)).utctimetuple())
        )

    async def put_last_exp_dt(self, user_name: str, exp_dt_timestamp: int) -> None:
        self.data[user_name] = exp_dt_timestamp


class TokenServiceDep():
    def __init__(
        self,
        secret: str,
        storage_class: StorageInterface = MemoryStorage,
        storage_config: Optional[dict[str, Any]] = None,
        access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT,
        refresh_token_expire_minutes: int = REFRESH_TOKEN_EXPIRE_MINUTES_DEFAULT,
    ):
        self.service = TokenService(
            secret=secret,
            storage_class=storage_class,
            storage_config=storage_config,
            access_token_expire_minutes=access_token_expire_minutes,
            refresh_token_expire_minutes=refresh_token_expire_minutes,
        )

    def __call__(self) -> TokenService:
        return self.service