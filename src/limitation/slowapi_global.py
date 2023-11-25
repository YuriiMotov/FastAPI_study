from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import REDIS_HOST, REDIS_PORT

# Rate limit 5 requests per minute for every URL (could be overriden)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    default_limits=["5/minute"]
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIASGIMiddleware)


@app.get("/home")
async def homepage(request: Request):
    return "test"


@app.get("/varpath/{num}")
async def varpath(request: Request, num: str):
    return {"num": num}


@app.get("/custom-limit")
@limiter.limit("10/minute")
async def custom_limit(request: Request):
    return "Custom limit"


@app.get("/unlimited")
@limiter.exempt
async def unlimited(request: Request):
    return "Unlimit!"

