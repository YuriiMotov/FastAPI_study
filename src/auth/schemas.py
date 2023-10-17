import uuid
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True  # UserWarning: Valid config keys have changed in V2:
                                # 'orm_mode' has been renamed to 'from_attributes'


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    # fields from BaseUserUpdate
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

    # additional fields
    username: Optional[str] = None
    role_id: Optional[int] = None

    # add logic to `create_update_dict` method to prevent user change their own `role_id`.
    # superuser still will be able to change it
    def create_update_dict(self):
        data = super().create_update_dict()
        if 'role_id' in data:
            data.pop('role_id')
        return data
