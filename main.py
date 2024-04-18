from fastapi import FastAPI
from routers import pc
from routers import  jwt_auth_users



app = FastAPI()

#Routes

app.include_router(pc.router)
app.include_router(jwt_auth_users.router)

