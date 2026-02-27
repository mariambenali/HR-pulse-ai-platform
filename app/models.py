from sqlalchemy import Column, String, Integer
from .database import Base, engine




Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email= Column(String(255), unique=True, nullable=False)
    hashedpassword=Column(String, nullable=False)


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String(255), nullable=False)
    skills = Column(String(255), nullable=False)