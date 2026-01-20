from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

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
