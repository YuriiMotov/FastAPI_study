from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = 'keycloak-auth.env'


class Settings(BaseSettings):

    keycloak_server_url: str
    keycloak_client_id: str
    keycloak_realm_name: str
    keycloak_client_secret_key: str

    # For tests
    keycloak_test_realm_name: str = 'test_realm'
    keycloak_test_realm_admin_client_id: str = 'admin-cli'
    keycloak_test_realm_admin_name: str = 'test_admin'
    keycloak_test_realm_admin_pwd: str = 'test_admin_pwd'
    keycloak_test_realm_user_client_id: str = 'end-user'


    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding="utf-8"
    )

config = Settings()