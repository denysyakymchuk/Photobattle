from fastapi import Depends, FastAPI, Response, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseSettings
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi_jwt_auth import AuthJWT

import models
from gen_token import gen_token, get_db
from gmail_sender import Email
from schemas import User

app = FastAPI()


@app.post("/")
def set_cookie(response: Response):
    response.set_cookie(key="cookie_name", value="cookie_value")
    return {"message": "Cookie set!"}


@app.get("/hello/{name}")
async def say_hello(response: Response, name: str, cookies: str = None):
    print(cookies)
    if cookies:
        return {"message": f"{cookies}"}
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
def login(gmail: str, password: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):

    gmail = credentials.gmail
    password = credentials.password
    print(gmail)
    print(password)
    user = db.query(models.User).filter(models.User.email == gmail).first()

    if user.password == password:
        access_token = AuthJWT.create_access_token(subject=gmail)
        return {"access_token": access_token}

    else:
        return {'message': 'Email or password is not valid'}
