from fastapi import FastAPI
from routers import pc
from routers import  jwt_auth_users
from pydantic import BaseModel
from jose import jwt 
from passlib.context import CryptContext


app = FastAPI()

#Routes

app.include_router(pc.router)
app.include_router(jwt_auth_users.router)

