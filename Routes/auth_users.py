from fastapi import FastAPI
from Routes import users
from Routes import pc
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    full_name:str
    mail: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Marcos":{
        "username": "Helioz",
        "full_name": "Marcos Duque",
        "email": "marcosjduque2@gmail.com",
        "disabled": False,
        "password": "123456" 
    },
    "Sofi":{
        "username": "Sofi",
        "full_name": "Sofi Avendaño",
        "email": "marcosjduque3@gmail.com",
        "disabled": True,
        "password": "654321" 
    },
}
