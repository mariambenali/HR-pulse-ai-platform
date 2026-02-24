from sqlalchemy import Column, String, Integer, Boolean
from .database import Base, engine




Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email= Column(String(255), unique=True, nullable=False)
    hashedpassword=Column(String, nullable=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String(255), unique=True, nullable=False)
    skills = Column(String(255), unique=True, nullable=False)