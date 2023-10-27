import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.exc import SQLAlchemyError

from auth.router import router as router_auth
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from pages.router import router as router_pages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # `On startup` actions
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # `On shoutdown` actions


app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

origins = [
    "https://fastapi.tiangolo.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=[
        "Set-Cookie", "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin", "Authorization"
    ],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    print(exc)
    # Generate ticket for this problem and notify the admin
    ticket_id = 1 

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error occurred. Additional details were sent to the service " \
                    f"administrator. Ticket id: {ticket_id}"
        }
    )


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception):
    print(exc)
    # Generate ticket for this problem and notify the admin
    ticket_id = 1 

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error occurred. Additional details were sent to the service " \
                    f"administrator. Ticket id: {ticket_id}"
        }
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

# Tasks
app.include_router(
    router_tasks,
    prefix='/tasks',
    tags=['tasks']
)


# Pages
app.include_router(
    router_pages,
    prefix='/pages',
    tags=['pages']
)
