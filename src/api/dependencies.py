from typing import Annotated

from fastapi import Depends

from utils.unitofwork import UnitOfWork


UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
