from fastapi import APIRouter
from pydantic import BaseModel
from Routes import pc

router= APIRouter( prefix= "/user", tags=["Users"]) 
class User(BaseModel):
    mail: str
    password: str

users_list = [User( mail ="marcosjduque2@gmail.com", password = "12345")]

