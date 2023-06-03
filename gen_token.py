import time
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash
import random
import jwt

from config import SessionLocal


def gen_token(username):
    unique = generate_password_hash(password=username + str(random.randint(1, 1000)), salt_length=12)
    return unique


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
