from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    job_title: str = ""
    email: EmailStr
    phone: str = ""
    location: str = ""
    profile_summary: str = ""
    photo: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



# backend/app/schemas.py

class JobApplicationCreate(BaseModel):
    title: str
    username: str
    company: str
    location: Optional[str]
    experience: Optional[str]
    job_type: Optional[str]
    salary: Optional[str]
    source: Optional[str]
    url: str

class JobApplicationOut(JobApplicationCreate):
    id: int
    status: str
    created_at:  datetime

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str]
    source: Optional[str]
    url: Optional[str]
    status: str
    created_at: str  # ✅ STRING (fixes your error)

    class Config:
        from_attributes = True


class JobStatusUpdate(BaseModel):
    status: str

