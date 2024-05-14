from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "c2da719888838c06de8587a0bfc8ada4471e2ca92706484c4adaf647cf85bbc6"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


#Database example for testing
users_DB = {
    "RIADWaffle":{
        "username": "RIADWaffle",
        "full_name": "RIADWaffleDEV",
        "email": "Waffle@Dev.com",
        "disabled": False,
        "password": "$2a$12$bycyhYKGXl.qIj0/zAaDh.x4UnrEdyrd4dYXzw0qW/ImhKMXoLRYW",
    },
    "CubeMora":{
        "username": "CubeMora",
        "full_name": "CubeMoraDev",
        "email": "Mora@Dev.com",
        "disabled": True,
        "password": "$2a$12$4ogBquiLBDVO4KYxK2n3dezF3hi83stiMHe10lkAvuChogIds6412",
    }
}


#Check if the users is in the DB
def search_user_db(username: str):
        if username in users_DB:
            return UserDB(**users_DB[username])
        
def search_user(username: str):
        if username in users_DB:
            return User(**users_DB[username])



async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            detail="Invalid authentication", 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception

    return search_user(username)


#Chech the current user authentication
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            detail="Disabled Account", 
            status_code=status.HTTP_400_BAD_REQUEST, 
            headers={"WWW-Authenticate": "Bearer"})
    
    return user




#Ask for the input of the login
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_DB = users_DB.get(form.username)
    if not user_DB:
        raise HTTPException(detail="Incorrect username or password", 
                            status_code=status.HTTP_400_BAD_REQUEST)
    
    user= search_user_db(form.username)

    

    if not crypt.verify(form.password, user.password):
        raise HTTPException(detail="Incorrect username or password", 
                            status_code=status.HTTP_400_BAD_REQUEST)
    
    

    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


#Check the Current authenticated user
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user