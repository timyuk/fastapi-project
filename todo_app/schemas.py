from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskReturn(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None