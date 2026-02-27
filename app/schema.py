from pydantic import BaseModel, EmailStr





class UserCreate(BaseModel):
    email : EmailStr
    password : str 


class UserResponse(BaseModel):
    email : EmailStr
    password : str

    class Config:
        orm_mode = True


class PredictSalaryRequest(BaseModel):
    Rating: float
    Company_Name: str
    Industry: str
    Sector: str
    seniority: str
    job_role: str
    skills: str
    log_revenue: float
    company_age: float
    size_category: str


class PredictSalaryResponse(BaseModel):
    predicted_salary: float

    