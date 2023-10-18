from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate, OperationUpdate
from schemas import ErrorDetails

OPERATIONS_PER_PAGE = 3

router = APIRouter()


# Get operations with specific type
@router.get("/")
async def get_specific_operations(
    operation_type: str, page: int = 1, session: AsyncSession = Depends(get_async_session)
) -> list[OperationCreate]:
    query = select(Operation).where(Operation.type == operation_type) \
                .limit(OPERATIONS_PER_PAGE).offset(OPERATIONS_PER_PAGE * (page - 1))
    result = await session.scalars(query)
    return result.all()


# Create operation
@router.post(
    "/",
    responses={
        409: {
            "description": "Error. Operation with this id already exists",
            "model": ErrorDetails
        }
    }
)
async def add_specific_operation(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
) -> OperationCreate:
    try:
        op = Operation(**new_operation.model_dump())
        session.add(op)
        await session.commit()
        return op
    except IntegrityError:
        raise HTTPException(
            status_code=409, 
            detail=f"Error occurred. Operation with id={new_operation.id} already exists"
        )


# Create or replace operation
@router.put("/")
async def replace_specific_operation(
    operation_data: OperationCreate, session: AsyncSession = Depends(get_async_session)
) -> OperationCreate:
    op = await session.get(Operation, operation_data.id)
    if op:
        op.update_from_dict(operation_data.model_dump())
    else:
        op = Operation(**operation_data.model_dump())
        session.add(op)
    
    await session.commit()
    return op


# Edit operation
@router.patch(
    "/",
    responses={
        440: {
            "description": "Error. Operation with this id doesn't exists",
            "model": ErrorDetails
        }
    }
)
async def update_specific_operation(
    operation_data: OperationUpdate, session: AsyncSession = Depends(get_async_session)
) -> OperationCreate:
    op = await session.get(Operation, operation_data.id)
    if op:
        op.update_from_dict(operation_data.model_dump())
        await session.commit()
        return op
    else:
        raise HTTPException(
            status_code=440, 
            detail=f"Error occurred. Operation with id={operation_data.id} " \
                    "doesn't exists"
        )
