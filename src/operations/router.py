from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate, OperationUpdate

router = APIRouter()

# Get operations with specific type
@router.get("/")
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
) -> list[OperationCreate]:
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.scalars(query)
        return result.all()

    except Exception as e:
        ticket_id = 1 # Generate ticket for this problem and notify the admin
        raise HTTPException(
            status_code=500, 
            detail="Error occurred. Additional details were sent to the service " \
                    f"administrator. Ticket id: ticket_id"
        )


# Create operation
@router.post("/")
async def add_specific_operation(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
) -> OperationCreate:
    op = Operation(**new_operation.model_dump())
    session.add(op)
    await session.commit()
    return op


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
@router.patch("/")
async def update_specific_operation(
    operation_data: OperationUpdate, session: AsyncSession = Depends(get_async_session)
) -> OperationCreate:
    op = await session.get(Operation, operation_data.id)
    if op:
        op.update_from_dict(operation_data.model_dump())
        await session.commit()
        return op
