from .models import User, Job
from .schema import UserCreate, UserResponse, PredictSalaryRequest, PredictSalaryResponse, JobSearchRequest
from ml.src.prediction import load_model
from .security import hash_password, verify_password
from .database import SessionLocal, engine, Base
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from jose import jwt
from dotenv import load_dotenv
import pandas as pd
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor



Base.metadata.create_all(bind=engine)


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()


#créer un provider
trace.set_tracer_provider(TracerProvider())

#exporter vers jaeger
otlp_exporter= OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)

span_processor= BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

#instrumenter Fastapi
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor.instrument(app)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBearer()

model = load_model()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hash_pwd = hash_password(user.password)
    new_user = User(
        email=user.email,
        hashedpassword=hash_pwd, 

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

    
@app.post("/login")  
def login(user: UserResponse, db: Session = Depends(get_db)):
    user_login = db.query(User).filter(User.email == user.email).first()
    
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, user_login.hashedpassword):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    payload = {
        "sub": user_login.email,
        "user_id": user_login.id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}



@app.get("/token") 
def verify_token(auth: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = auth.credentials  
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
            
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
    


@app.post("/salary_predict", response_model= PredictSalaryResponse)
def salary_predict(payload: PredictSalaryRequest, reccurent_user: User= Depends(verify_token), db: Session= Depends(get_db)):
    
    input_data = pd.DataFrame([payload.dict()])
    prediction= model.predict(input_data)

    new_job = Job(
        job_role = payload.job_role,
        skills = payload.skills
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {"predicted_salary": float(prediction[0])}



@app.post("/search_jobs")
def search_jobs(payload: JobSearchRequest, reccurent_user: User= Depends(verify_token), db: Session = Depends(get_db)):

    filters = []

    for skill in payload.skills:
        filters.append(Job.skills.ilike(f"%{skill}%"))

    jobs = db.query(Job).filter(or_(*filters)).all()

    return jobs