import asyncio
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate, OperationRead, OperationUpdate
from schemas import ErrorDetails

OPERATIONS_PER_PAGE = 3

router = APIRouter()


# Get operations with specific type
@router.get("/")
@cache(expire=5)
async def get_specific_operations(
    operation_type: str, page: int = 1, session: AsyncSession = Depends(get_async_session)
) -> list[OperationRead]:
    query = select(Operation).where(Operation.type == operation_type) \
                .limit(OPERATIONS_PER_PAGE).offset(OPERATIONS_PER_PAGE * (page - 1))
    result = await session.scalars(query)
    return result.all()


# Long operation
@router.get("/long-operation")
@cache(expire=30)
async def process_long_operations() -> str:
    await asyncio.sleep(5)
    return "results"

# Long operation with client-side caching
@router.get("/long-operation2")
async def process_long_operations2(response: Response) -> str:
    response.headers["Cache-Control"] = "max-age=60"
    await asyncio.sleep(5)
    return "results"


# Create operation
@router.post(
    "/",
    status_code=201
)
async def add_specific_operation(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
) -> OperationRead:
    op = Operation(**new_operation.model_dump())
    session.add(op)
    await session.commit()
    return op


# Create or replace operation
@router.put(
    "/{operation_id}",
    responses={
        440: {
            "description": "Error. An operation with this id doesn't exists",
            "model": ErrorDetails
        }
    }
)
async def replace_specific_operation(
    operation_id: int,
    operation_data: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
) -> OperationRead:
    op = await session.get(Operation, operation_id)
    if op:
        op.update_from_dict(operation_data.model_dump())
    else:
        raise HTTPException(
            status_code=440, 
            detail=f"Error occurred. An operation with id={operation_id} " \
                    "doesn't exists"
        )
    
    await session.commit()
    return op


# Edit operation
@router.patch(
    "/{operation_id}",
    responses={
        440: {
            "description": "Error. An operation with this id doesn't exists",
            "model": ErrorDetails
        }
    }
)
async def update_specific_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> OperationRead:
    op = await session.get(Operation, operation_id)
    if op:
        op.update_from_dict(operation_data.model_dump())
        await session.commit()
        return op
    else:
        raise HTTPException(
            status_code=440, 
            detail=f"Error occurred. An operation with id={operation_id} " \
                    "doesn't exists"
        )
