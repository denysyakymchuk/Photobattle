from fastapi import Depends, FastAPI, Response, Request
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from session import Session

import models
from gen_token import gen_token, get_db
from gmail_sender import Email
from schemas import User

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.post("/")
def set_cookie(response: Response):
    response.set_cookie(key="cookie_name", value="cookie_value")
    return {"message": "Cookie set!"}


@app.post("/get_cookie")
def get_cookie(request: Request, response: Response, cookies: str = None):
    request = {"_user_id": 1, }
    print(Session(**request).check_time_spam())
    if cookies:
        return {"message": "Cookie received!", "cookies": cookies}
    else:
        return {"message": "No cookie received!"}


# @app.get("/")
# async def root(response: Response, db: Session = Depends((get_db))):
#
#     response.set_cookie(key='lol', value='lololol')
#
#     mod = delete(models.User)
#     db.execute(mod)
#
#     db.commit()
#     return {"message": "Hello World"}


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
def login(request: Request, db: Session = Depends(get_db)):
    print(request.user)
    gmail, password = ''
    print(gmail)
    print(password)
    user = db.query(models.User).filter(models.User.email == gmail).first()

    if user.password == password:
        ch = Session().login_user(user.id)

        if ch:
            user.block = 1
            return {'message': 'Account is block'}
        else:
            return True

    else:
        return {'message': 'Email or password is not valid'}
