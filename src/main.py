from typing import Annotated
from fastapi import Depends, FastAPI

from auth.router import auth_router
from items.router import items_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(items_router)

    



