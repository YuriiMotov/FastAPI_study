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


class TaskSchemaEdit(BaseModel):
    author_id: int
    assignee_id: int


class TaskHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    task_id: int
    previous_assignee_id: int
    new_assignee_id: int


class TaskHistorySchemaAdd(BaseModel):
    task_id: int
    previous_assignee_id: int
    new_assignee_id: int