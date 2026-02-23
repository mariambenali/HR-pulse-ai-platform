from pydantic import BaseModel, EmailStr





class UserCreate(BaseModel):
    email : EmailStr
    password : str 


class UserResponse(BaseModel):
    email : EmailStr
    password : str

    class Config:
        orm_mode = True


class QueryRequest(BaseModel):
    id_job: int
    job_title : str
    skills_extracted: str

class QueryResponse(BaseModel):
    salary_predict: float