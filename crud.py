from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate

def get_all_tasks(db: Session):
    return db.query(Task).all()

def add_task(db: Session, task_data: TaskCreate):
    new_task = Task(**task_data.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        if task_data.judul is not None:
            task.judul = task_data.judul
        if hasattr(task_data, "deskripsi") and task_data.deskripsi is not None:
            task.deskripsi = task_data.deskripsi
        if hasattr(task_data, "deadline") and task_data.deadline is not None:
            task.deadline = task_data.deadline
        if hasattr(task_data, "done") and task_data.done is not None:
            task.done = task_data.done
        if hasattr(task_data, "pushover") and task_data.pushover is not None:
            task.pushover = task_data.pushover
    
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
