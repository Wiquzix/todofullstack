from datetime import datetime
from pydantic import BaseModel


class TaskCreate(BaseModel):
  title: str
class TaskUpdate(BaseModel):
  title: str
  completed: bool
class TaskBase(TaskCreate):
   id: str
   created_at: datetime
   completed: bool
class Task(TaskBase):
  owner_id: str

