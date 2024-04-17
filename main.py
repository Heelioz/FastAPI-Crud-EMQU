from fastapi import FastAPI
from Routes import users
from Routes import pc
from pydantic import BaseModel

app = FastAPI()

#Routes
app.include_router(users.router)
app.include_router(pc.router)