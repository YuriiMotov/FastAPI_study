from pydantic import BaseModel, ConfigDict


class TaskSchemaBase(BaseModel):
    title: str
    author_id: int
    assignee_id: int


class TaskSchema(TaskSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TaskSchemaAdd(TaskSchemaBase):
    pass


class TaskSchemaEdit(BaseModel):
    assignee_id: int



class TaskHistorySchemaBase(BaseModel):
    task_id: int
    previous_assignee_id: int
    new_assignee_id: int


class TaskHistorySchema(TaskHistorySchemaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class TaskHistorySchemaAdd(TaskHistorySchemaBase):
    pass