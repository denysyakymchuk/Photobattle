from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session

import models
from config import app
from gen_token import gen_token, get_db
from gmail_sender import Email
from schemas import User


@app.get("/")
async def root(db: Session = Depends((get_db))):
    mod = delete(models.User)
    db.execute(mod)

    db.commit()
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/registration")
async def registration(user: User, db: Session = Depends(get_db)):
    print(user)
    if db.query(models.User).filter(models.User.email == user.email).first():
        return {"message": "Email already use"}
    try:
        unique = gen_token(user.username)
        db_user = models.User(username=user.username, password=user.password,
                              email=user.email, gender=user.gender, unique=unique)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        Email().verif(user.email, unique)
    except Exception as sms:
        pass
    finally:
        return {"message": 'user is write'}


@app.get("/verification-email/{key}")
def verification_gmail(key: str, db: Session = Depends(get_db)):
    print("nie jestem lolololololololololololo")
    user = db.query(models.User).filter(models.User.unique == key).first()
    if user:
        user.active = True
        db.commit()
        db.refresh(user)
        print("jestem")
        return {"message": "Failed activation"}
    else:
        return {"message": "Failed activation"}

@app.post("/login")
def login(gmail: str, password: str, db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.email == gmail).first()



