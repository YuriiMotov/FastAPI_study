from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from auth.router import router as router_auth
from operations.router import router as router_operation


app = FastAPI(
    title="Trading App"
)


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
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
