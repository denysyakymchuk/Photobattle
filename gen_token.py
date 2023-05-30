import time
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash
import random
import jwt

JWT_SECRET = '52704f664e057ed33e984dd5c3f291c8'
JWT_ALGORITH = 'HS256'


def gen_token(username):
    unique = generate_password_hash(password=username + str(random.randint(1, 1000)), salt_length=12)
    return unique


def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITH)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITH)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}