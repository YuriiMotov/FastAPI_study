from typing import Annotated

from fastapi import Depends

from utils.unitofwork import SQLAUnitOfWork


UOWDep = Annotated[SQLAUnitOfWork, Depends(SQLAUnitOfWork)]
