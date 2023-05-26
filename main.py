from fastapi import FastAPI
from models import *
from schemas import User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}\

@app.get("/registration")
async def registration(user: User):
    return {"message": f"Hello {}"}
