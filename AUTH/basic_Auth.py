from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "WafflesDev",
    },
    "CubeMora":{
        "username": "CubeMora",
        "full_name": "CubeMoraDev",
        "email": "Mora@Dev.com",
        "disabled": True,
        "password": "MoritaDev",
    }
}



#Check if the users is in the DB
def search_user_db(username: str):
        if username in users_DB:
            return UserDB(**users_DB[username])
        
def search_user(username: str):
        if username in users_DB:
            return User(**users_DB[username])


#Chech the current user authentication
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            detail="Invalid authentication", 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            headers={"WWW-Authenticate": "Bearer"})
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
    if not form.password == user.password:
        raise HTTPException(detail="Incorrect username or password", 
                            status_code=status.HTTP_400_BAD_REQUEST)
    
    return {"access_token": user.username, "token_type": "bearer"}


#Check the Current authenticated user
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user