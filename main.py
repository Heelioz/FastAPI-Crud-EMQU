from fastapi import FastAPI
from routers import pc, test
from routers import  jwt_bd

app = FastAPI()

#Routes

app.include_router(pc.router)
app.include_router(jwt_bd.router)
app.include_router(test.router)

