from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column (Integer, primary_key=True, index=True)
    judul = Column (String, index=True)
    deskripsi = Column(String)
    deadline = Column(DateTime, nullable=True)
    done = Column(Boolean, default=False)
    pushover = Column(Boolean, default=False)