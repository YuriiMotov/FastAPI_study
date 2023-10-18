from pydantic import BaseModel


class ErrorDetails(BaseModel):
    detail: str