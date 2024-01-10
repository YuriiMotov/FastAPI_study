from fastapi.testclient import TestClient
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection, KeycloakOpenID
import pytest
from uuid import uuid4

from main import app
from auth.keycloak_dep import keycloak_oid_dep
from config_reader import config

client = TestClient(app)



# Override `keycloak_oid_dep` dependency

_keycloak_openid = KeycloakOpenID(
    server_url=config.keycloak_server_url,
    client_id=config.keycloak_test_realm_user_client_id,
    realm_name=config.keycloak_test_realm_name,
)

def keycloak_oid_dep_override():
    return _keycloak_openid

app.dependency_overrides[keycloak_oid_dep] = keycloak_oid_dep_override


# Keycloak fixtures

@pytest.fixture(scope="session")
def keycloak_admin():
    keycloak_connection = KeycloakOpenIDConnection(
        server_url=config.keycloak_server_url,
        username=config.keycloak_test_realm_admin_name,
        password=config.keycloak_test_realm_admin_pwd,
        realm_name=config.keycloak_test_realm_name,
        user_realm_name=config.keycloak_test_realm_name,
        client_id=config.keycloak_test_realm_admin_client_id,
        verify=True
    )
    return KeycloakAdmin(connection=keycloak_connection)


@pytest.fixture(scope="session")
def keycloak_create_user(keycloak_admin: KeycloakAdmin):
    user_email = f"{uuid4()}@example.com"
    user_data = {
        "email": user_email,
        "username": user_email,
        "enabled": True,
        "firstName": "Example",
        "lastName": "Example",
        "credentials": [{"value": str(uuid4()), "type": "password",}]
    }
    new_user = keycloak_admin.create_user(user_data)
    yield user_data
    keycloak_admin.delete_user(new_user)


@pytest.fixture(scope="function")
def keycloak_valid_tokens(keycloak_create_user: dict):
    user_data = keycloak_create_user.copy()

    keycloak_oid = keycloak_oid_dep_override()
    tokens = keycloak_oid.token(
        username=user_data["username"], password=user_data["credentials"][0]["value"]
    )
    yield tokens


@pytest.fixture(scope="function")
def keycloak_privileged_tokens():

    keycloak_oid = keycloak_oid_dep_override()
    tokens = keycloak_oid.token(
        username=config.keycloak_test_realm_admin_name,
        password=config.keycloak_test_realm_admin_pwd,
        scope="openid me items"
    )
    return tokens

