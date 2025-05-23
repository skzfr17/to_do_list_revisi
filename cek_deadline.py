import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task, Base
import saas  # pastikan file saas.py memiliki fungsi send_notification

DATABASE_URL = "sqlite:///./task.db"

# Setup DB session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cek_deadline():
    session = SessionLocal()
    try:
        now = datetime.datetime.now()
        satu_hari = datetime.timedelta(days=1)

        print(f"[{now.strftime('%Y-%m-%d %H:%M')}] Mengecek tugas yang deadline...")

        # Task yang deadline dalam 1 hari ke depan dan belum selesai
        upcoming_tasks = session.query(Task).filter(
            Task.done == False,
            Task.deadline != None,
            Task.deadline <= now + satu_hari,
            Task.deadline >= now
        ).all()

        # Task yang sudah lewat deadline dan belum selesai
        overdue_tasks = session.query(Task).filter(
            Task.done == False,
            Task.deadline != None,
            Task.deadline < now
        ).all()

        semua_task = upcoming_tasks + overdue_tasks

        if not semua_task:
            print("Tidak ada tugas yang perlu diingatkan saat ini.")
        else:
            print(f"⚠️ Ditemukan {len(semua_task)} tugas yang perlu diperhatikan.")
            for task in semua_task:
                deadline_str = task.deadline.strftime('%Y-%m-%d %H:%M')
                if task.pushover:
                    pesan = f"Pengingat: Tugas '{task.judul}' akan deadline pada {deadline_str}"
                    print(f"Mengirim notifikasi: {pesan}")
                    saas.send_notification(pesan)
                else:
                    print(f"Tugas '{task.judul}' deadline {deadline_str}, tapi notifikasi pushover dimatikan.")

    finally:
        session.close()

if __name__ == "__main__":
    cek_deadline()
