from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
   username: str
   password: str
class UserResponse(BaseModel):
  id: str
  username: str
class User(UserResponse):
  hashed_password: str
class Token(BaseModel):
   access_token: str
   token_type: str

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
