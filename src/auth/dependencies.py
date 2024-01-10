from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError
from keycloak import KeycloakOpenID

from auth.keycloak_dep import keycloak_oid_dep, keycloak_public_key_dep



class Scopes(Enum):
    me: str = "me"
    items: str = "items"

app_scopes = {
    Scopes.me.value: "Read information about the current user.",
    Scopes.items.value: "Read items."
}


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8080/realms/test/protocol/openid-connect/token",
    scopes=app_scopes
)


def current_user_dep(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: SecurityScopes,
    keycloak_oid: Annotated[KeycloakOpenID, Depends(keycloak_oid_dep)],
    keycloak_public_key: Annotated[str, Depends(keycloak_public_key_dep)]
):
    options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
    try:
        token_info = keycloak_oid.decode_token(
            token=token, key=keycloak_public_key, options=options
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_scopes = token_info["scope"].split()
    for required_scope in security_scopes.scopes:
        if required_scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return token_info["sub"]