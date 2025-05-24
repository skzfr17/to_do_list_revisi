from sqlalchemy.orm import Session
from backend.models import Task, User
from backend.schemas import TaskCreate, TaskUpdate, UserCreate
from typing import Optional
from passlib.context import CryptContext
# ===== TASK CRUD =====

def get_all_tasks(db: Session):
    return db.query(Task).all()

def add_task(db: Session, task_data: TaskCreate):
    data = task_data.dict()
    data['notifikasi'] = False
    new_task = Task(**data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        if task_data.judul is not None:
            task.judul = task_data.judul
        if task_data.deskripsi is not None:
            task.deskripsi = task_data.deskripsi
        if task_data.deadline is not None:
            task.deadline = task_data.deadline
        if task_data.done is not None:
            task.done = task_data.done
        if task_data.pushover is not None:
            task.pushover = task_data.pushover
        if task_data.notifikasi is not None:
            task.notifikasi = task_data.notifikasi
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task

# === Konfigurasi hashing password ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ===== USER CRUD =====

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pw,
        pushover_user_key=user_data.pushover_user_key
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None