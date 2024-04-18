from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM ="HS256"
ACCESS_TOKEN_DURATION = 1

router= APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name:str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "marcosjduque2@gmail.com":{
        "username": "Helioz",
        "full_name": "Marcos Duque",
        "email": "marcosjduque2@gmail.com",
        "disabled": False,
        "password": "$2a$12$7OxAqIjlQ4jLEBrep1tZs.1LNVCvLJHHQRq7Dv4O3bYqlzmPy0.Ry" 
    },
    "marcosjduque3@gmail.com":{
        "username": "Sofi",
        "full_name": "Sofi Avendaño",
        "email": "marcosjduque3@gmail.com",
        "disabled": True,
        "password": "654321" 
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail ="Usuario incorrecto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
         raise HTTPException(
            status_code=400, detail ="Contraseña incorrecta")
    

  
    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.email, 
                    "exp": expired,
                    }
    
    return{"access_token": access_token , "token_type": "bearer"}
    