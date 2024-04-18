from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymongo import MongoClient

# MongoDB connection details (replace with your actual credentials)
MONGODB_URI = "mongodb+srv://EMQU:test@cluster0.jyg0ozp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "test"
USER_COLLECTION = "users"

client = MongoClient(MONGODB_URI)
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
    user = user_collection.find_one({"email": username})
    if user:
        return User(**user)
    return None


async def search_user_db(username: str):
    user = user_collection.find_one({"email": username})
    if user:
        return UserDB(**user)
    return None





async def auth_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"www-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"www-Authenticate": "Bearer"},
        )

    user = await search_user(email)
    return user


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
            headers={"www-Authenticate": "Bearer"},
        )

    return user


@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = await search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Extract username and email from form
    username = form.username
    email = user_db.email

    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": email, 
                    "exp": expired,
                    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }




@router.post("/signup")
async def signup(user_data: dict):

    existing_email = await search_user(user_data["email"])

    if existing_email:
        raise HTTPException(status_code=400, detail="Correo electrónico ya existe")

    # Create UserDB object (include password)
    user_db = UserDB(**user_data)

    # Hash the password before saving
    user_db.password = crypt.hash(user_db.password)

    # Convert UserDB object to dictionary
    user_dict = user_db.dict()

    # Insert the user document with the hashed password
    user_collection.insert_one(user_dict)

    return {"message": "Usuario creado exitosamente"}
