from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationUpdate(BaseModel):
    id: int
    quantity: Optional[str] = None
    figi: Optional[str] = None
    instrument_type: Optional[str] = None
    date: Optional[datetime] = None
    type: Optional[str] = None