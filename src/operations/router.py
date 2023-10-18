from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate, OperationUpdate

router = APIRouter()


@router.get("/")
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.scalars(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/")
async def add_specific_operations(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    op = Operation(**new_operation.model_dump())
    session.add(op)
    await session.commit()
    return {"status": "success"}


@router.put("/")
async def replace_specific_operation(
    operation_data: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    op = await session.get(Operation, operation_data.id)
    if op:
        op.update_from_dict(operation_data.model_dump())
    else:
        op = Operation(**operation_data.model_dump())
        session.add(op)
    
    await session.commit()
    return {"status": "success"}


@router.patch("/")
async def update_specific_operation(
    operation_data: OperationUpdate, session: AsyncSession = Depends(get_async_session)
):
    op = await session.get(Operation, operation_data.id)
    if op:
        op.update_from_dict(operation_data.model_dump())
        await session.commit()
        return {"status": "success"}
    else:
        return {"status": "error"}