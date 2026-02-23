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
    title : str

class QueryResponse(BaseModel):
    salary_predict: float