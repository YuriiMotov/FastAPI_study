from datetime import datetime, timedelta

from freezegun import freeze_time
from keycloak.exceptions import KeycloakPostError
import pytest

from tests.conftest import client, keycloak_oid_dep_override


def test_login(keycloak_create_user: dict[str, str]):
    """ Login with username and password, get tokens """
    
    user_name = keycloak_create_user["username"]
    user_password = keycloak_create_user["credentials"][0]["value"]

    keycloak_oid = keycloak_oid_dep_override()

    tokens = keycloak_oid.token(
        username=user_name, password=user_password
    )
    assert tokens is not None
    assert tokens.get("access_token") is not None
    assert tokens.get("refresh_token") is not None


def test_protected_endpoint_not_authenticated():
    """ Requesting protected endpoint without valid access token """
    res = client.get("/auth/me/")
    assert res.status_code == 401


def test_protected_endpoint(keycloak_valid_tokens: dict):
    """ Requesting protected endpoint with valid access token """
    access_token = keycloak_valid_tokens["access_token"]
    # print('---', access_token, '---')
    res = client.get("/auth/me/", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200


def test_protected_endpoint_no_rights(keycloak_valid_tokens: dict):
    """
        Requesting protected endpoint with valid access token, but without rights (scope)
    """
    access_token = keycloak_valid_tokens["access_token"]
    # print('---', access_token, '---')
    res = client.get("/items/", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 401


def test_protected_endpoint_having_rights(keycloak_privileged_tokens: dict):
    """
        Requesting protected endpoint with valid access token,
        with additional rights (scope).

        Privileged user has to have 'items-manager` role to pass this test.
    """
    access_token = keycloak_privileged_tokens["access_token"]

    res = client.get("/items/", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200


def test_refresh_token(keycloak_valid_tokens: dict):
    """ Getting new access token by sending request with refresh token """
    access_token = keycloak_valid_tokens["access_token"]
    refresh_token = keycloak_valid_tokens["refresh_token"]

    keycloak_oid = keycloak_oid_dep_override()

    tokens = keycloak_oid.refresh_token(refresh_token=refresh_token)
    assert tokens is not None
    assert tokens.get("access_token") is not None
    assert tokens.get("refresh_token") is not None

    assert tokens.get("access_token") != access_token
    assert tokens.get("refresh_token") != refresh_token


def test_refresh_token_rotation(keycloak_valid_tokens: dict):
    """ Getting new access token by sending request with refresh token """
    access_token = keycloak_valid_tokens["access_token"]
    refresh_token = keycloak_valid_tokens["refresh_token"]

    keycloak_oid = keycloak_oid_dep_override()

    tokens = keycloak_oid.refresh_token(refresh_token=refresh_token)
    assert tokens is not None
    assert tokens.get("access_token") is not None
    assert tokens.get("refresh_token") is not None

    # Trying to use the (already invalidated) refresh token a second time
    with pytest.raises(KeycloakPostError):
        tokens = keycloak_oid.refresh_token(refresh_token=refresh_token)


def test_logout(keycloak_valid_tokens: dict):
    """ Getting the refresh token invalidated via calling the logout endpoint """
    access_token = keycloak_valid_tokens["access_token"]
    refresh_token = keycloak_valid_tokens["refresh_token"]

    keycloak_oid = keycloak_oid_dep_override()

    keycloak_oid.logout(refresh_token=refresh_token)

    # Trying to use the (already invalidated) refresh token
    with pytest.raises(KeycloakPostError):
        tokens = keycloak_oid.refresh_token(refresh_token=refresh_token)


def test_invalid_access_token(keycloak_valid_tokens: dict):
    """ Requesting protected endpoint sending invalid access token """
    access_token = keycloak_valid_tokens["access_token"]

    with freeze_time(datetime.now() + timedelta(minutes=10)):
        res = client.get("/auth/me/", headers={"Authorization": f"Bearer {access_token}"})
        assert res.status_code == 401

