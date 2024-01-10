from typing import Annotated
from functools import lru_cache

from fastapi import Depends
from keycloak import KeycloakOpenID

from config_reader import config


# Configure client
_keycloak_openid = KeycloakOpenID(
    server_url=config.keycloak_server_url,
    client_id=config.keycloak_client_id,
    realm_name=config.keycloak_realm_name,
    client_secret_key=config.keycloak_client_secret_key
)

def keycloak_oid_dep():
    return _keycloak_openid


@lru_cache
def keycloak_public_key_dep(
    keycloak_oid: Annotated[KeycloakOpenID, Depends(keycloak_oid_dep)]
):
    return (
        "-----BEGIN PUBLIC KEY-----\n" + 
        keycloak_oid.public_key() + 
        "\n-----END PUBLIC KEY-----"
    )
        
