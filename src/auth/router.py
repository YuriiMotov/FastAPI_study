from typing import Annotated

from fastapi import APIRouter, Depends, Security
from keycloak import KeycloakOpenID

from auth.keycloak_dep import keycloak_oid_dep
from auth.dependencies import oauth2_scheme, current_user_dep, Scopes


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/me/")
def get_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    current_user: Annotated[dict, Security(current_user_dep, scopes=[Scopes.me.value])],
    keycloak_oid: Annotated[KeycloakOpenID, Depends(keycloak_oid_dep)]
):
    user_info = keycloak_oid.userinfo(token)
    return user_info
