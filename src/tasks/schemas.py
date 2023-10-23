from pydantic import BaseModel


class CeleryTaskState(BaseModel):
    task_id: str
    state: str
    progress: int

