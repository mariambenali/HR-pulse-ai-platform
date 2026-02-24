from .models import User
from .schema import UserCreate, UserResponse, PredictSalaryRequest, PredictSalaryResponse
from ml.src.prediction import load_model
from .security import hash_password, verify_password
from .database import SessionLocal, engine, Base
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt
from dotenv import load_dotenv
import pandas as pd
import os





Base.metadata.create_all(bind=engine)



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()

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
def salary_predict(payload: PredictSalaryRequest, reccurent_user: User= Depends(verify_token), db: Session= Depends(get_db) ):
    
    input_data = pd.DataFrame([payload.dict()])
    prediction= model.predict(input_data)

    return {"predicted_salary": float(prediction[0])}
