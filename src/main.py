import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.exc import SQLAlchemyError

from auth.router import router as router_auth
from celery_monitor.monitor import celery_tasks_monitor
from operations.router import router as router_operation
from tasks.router import router as router_tasks

app = FastAPI(
    title="Trading App"
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    celery_tasks_monitor.aio_task = asyncio.create_task(celery_tasks_monitor.loop())


@app.on_event("shutdown")
async def shutdown():
    celery_tasks_monitor.stop()


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
