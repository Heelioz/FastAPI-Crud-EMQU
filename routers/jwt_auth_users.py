from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError 
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM ="HS256"
ACCESS_TOKEN_DURATION = 1
SECRET ="c1e3bfdf347f294e25553b0a918fb053b2fd6c858e039865e7fbf2e3b76698b1"

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

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str =Depends(oauth2)):

    try:
    
        email = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if email is None:
            raise HTTPException(
            status_code=401, 
            detail ="Credenciales de autenticacion invalidas", 
            headers={"www-Authenticate": "Bearer"}) 


    
    except JWTError:
        raise HTTPException(
            status_code=401, 
            detail ="Credenciales de autenticacion invalidas", 
            headers={"www-Authenticate": "Bearer"}) 
    
    return search_user(email)
    

async def current_user(user: User = Depends(auth_user)):
   
   if user.disabled:
        raise HTTPException(
            status_code=400, 
            detail ="Usuario Inactivo", 
            headers={"www-Authenticate": "Bearer"}) 
   
   return user

@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user
    

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
    
    return{"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}

