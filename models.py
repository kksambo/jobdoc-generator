
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    job_title = Column(String)
    email = Column(String, nullable=False)
    phone = Column(String)
    location = Column(String)
    profile_summary = Column(String)
    photo = Column(String)
# backend/app/models.py


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    source = Column(String, nullable=True)
    url = Column(String, nullable=False)
    status = Column(String, default="Applied")  # Applied, Interviewed, Rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())



