from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

##########################################################################################
# Dependancy with yield

async def func_with_yield() -> str:
    print("Before yield")
    yield "value"
    print("After yield")

@app.get("/dependancy-with-yield")
def test_dependancy_with_yield(dependancy: str = Depends(func_with_yield)) -> str:
    print("Inside the route")
    print(f"{dependancy=}")
    return "Take a look at the console"



##########################################################################################
# Dependancy with parameters

def func_with_params(offset: int = 0, cnt: int = 10) -> dict[str, int]:
    return {"offset": offset, "cnt": cnt}


@app.get("/dependancy-with-params")
def test_dependancy_with_params(
    params: dict[str, int] = Depends(func_with_params)
) -> str:
    return f"{params=}"


# You can define how to pass these parameters
@app.get("/dependancy-with-params-in-path/{offset}/{cnt}")
def test_dependancy_with_params(
    params: dict[str, int] = Depends(func_with_params)
) -> str:
    return f"{params=}"


##########################################################################################
# Dependancy as a class

class Params():
    def __init__(self, offset: int = 0, cnt: int = 10):
        self.offset = offset
        self.cnt = cnt
    
    def __repr__(self):
        return f"{self.__class__.__name__}(offset={self.offset}, cnt={self.cnt})"


@app.get("/dependancy-with-params-class")
def test_dependancy_with_params_class(
    params: Params = Depends(Params)
) -> str:
    return f"{params=}"


##########################################################################################
# Class call
# Request

class AuthGuard():
    def __init__(self, name: str):
        self.name = name
    
    def __call__(self, request: Request):
        if "secret_cookie" not in request.cookies:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        # Check whether the user is aothorized to get this information
        return True


auth_guard_payments = AuthGuard("Payments")

@app.get("/payments")
def get_payments(authorized: bool = Depends(auth_guard_payments)) -> str:
    return "Payments information"


##########################################################################################
# Dependancies in FastAPI endpoint

@app.get("/payments-2", dependencies=[Depends(auth_guard_payments)])
def get_payments() -> str:
    return "Payments information 2"


##########################################################################################
# Dependancies in FastAPI router

router = APIRouter()

@router.get("/")
def get_payments() -> str:
    return "Payments information 3"

app.include_router(
    router,
    prefix="/payments-3",
    dependencies=[Depends(auth_guard_payments)]
)


##########################################################################################
# Authorization via OAuth2 Bearter and Password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth2-tests/token")

oauth2_router = APIRouter()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@oauth2_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@oauth2_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@oauth2_router.get("/users/me")
async def get_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


app.include_router(
    oauth2_router,
    prefix="/oauth2-tests",
    tags=["oauth2"]
)
