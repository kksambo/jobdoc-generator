from pydantic import BaseModel, EmailStr

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
