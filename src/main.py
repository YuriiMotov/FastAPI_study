import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.exc import SQLAlchemyError

from auth.router import router as router_auth
from chat.router import router as router_chat
from chat_v2.router import broadcast, router as router_chat_v2
from config import (
    REDIS_HOST, REDIS_PORT, WEB_APP_HOST, WEB_APP_PORT, API_APP_HOST, API_APP_PORT,
    API_APP_PATH
)
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from pages.router import router as router_pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # `On startup` actions
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await broadcast.connect()
    yield
    # `On shoutdown` actions
    await broadcast.disconnect()


##########################################################################################
# API app

api_app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

origins = [
    f"http://{WEB_APP_HOST}",
    f"https://{WEB_APP_HOST}",
    f"http://{WEB_APP_HOST}:{WEB_APP_PORT}",
    f"https://{WEB_APP_HOST}:{WEB_APP_PORT}",
]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=[
        "Set-Cookie", "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin", "Authorization"
    ],
)


@api_app.exception_handler(SQLAlchemyError)
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


@api_app.exception_handler(Exception)
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
api_app.include_router(
    router_auth,
    prefix='/auth',
    tags=['auth']
)

# Operations
api_app.include_router(
    router_operation,
    prefix='/operations',
    tags=['operations']
)

# Tasks
api_app.include_router(
    router_tasks,
    prefix='/tasks',
    tags=['tasks']
)


# Chat
api_app.include_router(
    router_chat,
    prefix='/chat',
    tags=['chat']
)

# Chat v2
api_app.include_router(
    router_chat_v2,
    prefix='/chat-v2',
    tags=['chat_v2']
)



##########################################################################################
# Web app

web_app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

web_app.mount("/static", StaticFiles(directory="static"), name="static")


@web_app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(exc)
    return HTMLResponse(
        status_code=500,
        content="<center><h1>Error occurred.</h1><h3>Please try later</h3></center>"
    )


# Pages
web_app.include_router(
    router_pages,
    prefix='/pages',
    tags=['pages']
)

# Mount API app as a subapplication
if (API_APP_HOST == WEB_APP_HOST) and (API_APP_PORT == WEB_APP_PORT):
    web_app.mount(API_APP_PATH, api_app, )
