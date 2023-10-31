from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import AsyncSession, get_async_session
from .auth import get_current_active_user
from . import auth
from . import schemas
from .orders_test import orders_router

app = FastAPI()

##########################################################################################
# Dependancy with yield

async def func_with_yield() -> str:
    print("Before yield")
    yield "value"
    print("After yield")

@app.get("/dependancy-with-yield")
def test_dependancy_with_yield(
    dependancy: Annotated[str, Depends(func_with_yield)]
) -> str:
    print("Inside the route")
    print(f"{dependancy=}")
    return "Take a look at the console"



##########################################################################################
# Dependancy with parameters

def func_with_params(offset: int = 0, cnt: int = 10) -> dict[str, int]:
    return {"offset": offset, "cnt": cnt}


@app.get("/dependancy-with-params")
def test_dependancy_with_params(
    params: Annotated[dict[str, int], Depends(func_with_params)]
) -> str:
    return f"{params=}"


# You can define how to pass these parameters
@app.get("/dependancy-with-params-in-path/{offset}/{cnt}")
def test_dependancy_with_params(
    params: Annotated[dict[str, int], Depends(func_with_params)]
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
    params: Annotated[Params, Depends(Params)]
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
def get_payments(authorized: Annotated[bool, Depends(auth_guard_payments)]) -> str:
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

oauth2_router = APIRouter()


@oauth2_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    form_data: OAuth2PasswordRequestForm = Depends()
):
    token = await auth.login(session=session, form_data=form_data)
    return token


@oauth2_router.post("/register", response_model=schemas.User)
async def register_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: schemas.UserCreate
):
    user = await auth.create_user(session=session, user_data=user_data)
    return user


@oauth2_router.get("/users/me", response_model=schemas.User)
async def get_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


app.include_router(
    oauth2_router,
    prefix="/oauth2-tests",
    tags=["oauth2"]
)


##########################################################################################
# Dependancies call order

app.include_router(
    orders_router,
    prefix="/orders-tests",
    tags=["orders-test"]
)
