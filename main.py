from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud, saas
from database import get_db
from schemas import Task,TaskCreate, TaskUpdate

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uji Coba API
@app.get("/")
def read_root():
    return {"message": "API is running"}

# Ambil semua task
@app.get("/tasks", response_model=List[Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)

# Tambahkan task baru
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = crud.add_task(db, task)
        if new_task.pushover:
            print("Mengirim notifikasi Pushover...")
            saas.send_notification(new_task.judul)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menambahkan task: {str(e)}")

# Perbarui task (bisa title, done, atau keduanya)# Perbarui task (bisa judul, deskripsi, done, pushover, deadline)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


# Hapus task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
