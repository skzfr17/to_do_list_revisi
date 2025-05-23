from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    deadline: Optional[datetime] = None
    done: Optional[bool] = False
    pushover: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    judul: Optional[str] = None
    deskripsi: Optional[str] = None
    deadline: Optional[datetime] = None
    done: Optional[bool] = None
    pushover: Optional[bool] = None

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
