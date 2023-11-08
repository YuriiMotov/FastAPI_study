from fastapi import APIRouter

from api.dependencies import UsersServiceDep
from schemas.users import UserSchemaAdd


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    users_service: UsersServiceDep
):
    user_id = await users_service.add_user(user)
    return {"user_id": user_id}


@router.get("")
async def get_users(
    users_service: UsersServiceDep
):
    users = await users_service.get_users()
    return users