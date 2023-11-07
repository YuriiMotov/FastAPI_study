from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_id: int
    assignee_id: int


class TaskSchemaAdd(BaseModel):
    title: str
    author_id: int
    assignee_id: int

    