from fastapi import FastAPI
from routers import pc
from routers import basic_auth_users
from pydantic import BaseModel


app = FastAPI()

#Routes

app.include_router(pc.router)
app.include_router(basic_auth_users.router)