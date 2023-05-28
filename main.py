from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from config import SessionLocal, engine
from models import *
from schemas import User

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/registration")
async def registration(user: User, db: Session = Depends(get_db)):
    print(user)
    db_user = models.User(username=user.username, password=user.password,
                          email=user.email, gender=user.gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": 'success'}
