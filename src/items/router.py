from typing import Annotated

from fastapi import APIRouter, Security

from auth.dependencies import current_user_dep, Scopes

items_router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@items_router.get("/")
def get_items(
    current_user: Annotated[
        dict,
        Security(current_user_dep, scopes=[Scopes.items.value])
    ],
):
    return ['item']

