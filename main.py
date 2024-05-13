from fastapi import FastAPI

# ROUTERS IMPORTS
from routers import Products



app = FastAPI()

#Add the routers to the main API
app.api_route(Products.router)

