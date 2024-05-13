from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class user(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


example_DB = {
    "RIADWaffle":{
        "username": "Waffle",
        "Full_name": "RIADWaffle",
        "email": "Waffle@Dev.com",
        "disabled": False,
        "password": "WafflesDev",
    },
    "CubeMora":{
        "username": "Mora",
        "Full_name": "CubeMora",
        "email": "Mora@Dev.com",
        "disabled": True,
        "password": "MoritaDev",
    }
}