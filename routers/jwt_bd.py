from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymongo import MongoClient


MONGODB_URI = "mongodb+srv://EMQU:test@cluster0.jyg0ozp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
DATABASE_NAME = "test"
USER_COLLECTION = "users"

client = MongoClient(MONGODB_URI).test
db = client[DATABASE_NAME]
user_collection = db[USER_COLLECTION]

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "c1e3bfdf347f294e25553b0a918fb053b2fd6c858e039865e7fbf2e3b76698b1"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

async def search_user(username: str):
    user = user_collection.find_one({"username": username})
    if user:
        return User(**user)
    return None

async def search_user_by_email(email: str):
    user = user_collection.find_one({"email": email})
    if user:
        return UserDB(**user)
    return None

async def auth_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Credenciales de autenticación inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await search_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credenciales de autenticación inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=400, detail="Usuario Inactivo", headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = await search_user_by_email(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")

    # Debug data structure (optional)
    print(f"User data from DB: {user_db}")

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user_db.email, "exp": expired}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.post("/signup")
async def signup(user_data: dict):
  
    existing_user = await search_user(user_data["username"])
    existing_email = await search_user_by_email(user_data["email"])

    if existing_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya existe")

    if existing_email:
        raise HTTPException(status_code=400, detail="Correo electrónico ya existe")

    user_data["password"] = crypt.hash(user_data["password"])  # Hash password before saving

    user = User(**user_data)  # Create User object from validated data
    user_dict = user.dict()  # Convert User object to dictionary

    user_collection.insert_one(user_dict)  # Insert new user record

    return {"message": "Usuario creado exitosamente"}

