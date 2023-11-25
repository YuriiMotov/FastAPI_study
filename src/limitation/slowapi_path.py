from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import REDIS_HOST, REDIS_PORT

# Different rate limits for endpoints

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{REDIS_HOST}:{REDIS_PORT}"
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/home")
@limiter.limit("5/minute")
async def homepage(request: Request):
    return "test"


@app.get("/varpath/{num}")
@limiter.limit("3/minute")
async def varpath(request: Request, num: str):
    return {"num": num}


@app.get("/unlimited")
async def unlimited(request: Request):
    return "Unlimit!"
