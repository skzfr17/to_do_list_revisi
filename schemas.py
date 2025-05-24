from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# ==== USER ====

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    pushover_user_key: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    pushover_user_key: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    hashed_password: str

# ==== AUTH RESPONSE ====

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ==== TASK ====

class TaskBase(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    deadline: Optional[datetime] = None
    done: Optional[bool] = False
    pushover: Optional[bool] = False
    notifikasi: Optional[bool] = False

class TaskCreate(TaskBase):
    user_id: int

class TaskUpdate(BaseModel):
    judul: Optional[str] = None
    deskripsi: Optional[str] = None
    deadline: Optional[datetime] = None
    done: Optional[bool] = None
    pushover: Optional[bool] = None
    notifikasi: Optional[bool] = None

class Task(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
