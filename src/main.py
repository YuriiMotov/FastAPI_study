from fastapi import FastAPI

from auth.router import router as router_auth
from operations.router import router as router_operation


app = FastAPI(
    title="Trading App"
)

# Auth
app.include_router(
    router_auth,
    prefix='/auth',
    tags=['auth']
)

# Operations
app.include_router(
    router_operation,
    prefix='/operations',
    tags=['operations']
)