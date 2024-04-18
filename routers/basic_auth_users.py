from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router= APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456" 
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
        return UserDB(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
   user = search_user(token)
   if not user:
        raise HTTPException(
            status_code=401, 
            detail ="Credenciales de autenticacion invalidas", 
            headers={"www-Authenticate": "Bearer"})
   return user
       
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail ="Usuario incorrecto")
    
    user = search_user(form.username)
    if not form.password == user.password:
         raise HTTPException(
            status_code=400, detail ="Contraseña incorrecta")
    
    return{"access_token": user.email  , "token_type": "bearer"}
    
@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user
