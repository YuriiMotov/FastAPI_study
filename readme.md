# The example of using keycloak to authenticate users in FastAPI app.

This is a part of [this study project](https://github.com/YuriiMotov/FastAPI_study/tree/main#fastapi_study).

To make it works you need to run and configure Keycloak server.


## Keycloak server configuration:

**Attention: this configuration is not for production!**

1) Create new realm 'test_realm', open it (select in drop-down menu)

2) Create user 'test_admin' (Users -> Add user -> Name = 'test_admin' -> Create), set up password (Credentials -> Set password -> Fill password and confirmation -> Turn off 'Temporary' -> Press 'Save' -> Press 'Save password')

3) Assign 'realm-admin' role to 'test_admin' (test_admin -> Role mapping -> Assign role -> Filter by clients -> Check role 'realm-admin' -> Press 'Assign')

4) Create role 'items-manager' (Realm roles -> Create role -> Fill 'Role name' -> Press 'Save')

5) Assign 'items-manager' role to 'test_admin' (test_admin -> Role mapping -> Assign role -> Filter by realm roles -> Check role 'items-manager' -> Press 'Assign')

6) Create client 'end-user' (Clients -> Create client -> Enter 'end-user' in 'Clent name' field -> Press 'Next' -> Press 'Save')

7) Include 'Audience' into token for 'end-user' client (Clients -> end-user -> Client scopes -> end-user-dedicated -> Configure a new mapper -> Audience -> Fill 'Name' (client-id) -> Select 'Included clients' = 'end-user' -> Press 'Save')

8) Create scope 'me' (Client scopes -> Create client scope -> Fill 'Name' (me) -> Select 'Type' = 'Default' -> Press 'Save')

9) Create scope 'items' (Client scopes -> Create client scope -> Fill 'Name' (items) -> Select 'Type' = 'Optional' -> Press 'Save')

10) Map scope 'items' to user role 'items-manager' (Client scopes -> items -> Scope -> Assign role -> Select 'items-manager' -> Press 'Assign')

11) Map 'me' scope to Client (Client -> end-user -> Client scopes -> Add client scope -> Select 'me' -> Press 'Add' -> Select 'Default')

12) Map 'items' scope to Client (Client -> end-user -> Client scopes -> Add client scope -> Select 'items' -> Press 'Add' -> Select 'Optional')

13) Configure refresh token rotation (Realm settings -> Tokens -> 'Revoke Refresh Token' = Enabled -> Scroll to the bottom and press 'Save')


## ENV-file

1) Create 'keycloak-auth.env' inside you project's root directory

2) Past and adjust the configuration (if you followed the instructions above, to pass the tests you need to specify only 'keycloak_server_url' and 'keycloak_test_realm_admin_pwd'):

```
    keycloak_server_url='http://localhost:8080'
    keycloak_client_id='account'
    keycloak_realm_name='test_realm'
    keycloak_client_secret_key=''

    # For tests
    #keycloak_test_realm_name='test_realm'
    #keycloak_test_realm_admin_client_id='admin-cli'
    #keycloak_test_realm_admin_name='test_admin'
    keycloak_test_realm_admin_pwd='test_admin_pwd'
    #keycloak_test_realm_user_client_id:='end-user'
```


# Run tests

Create venv and execute commands:

`pip install -r requirments.txt`

`pytest tests`