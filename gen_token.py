from werkzeug.security import generate_password_hash
import random


def gen_token(username):
    unique = generate_password_hash(password=username + str(random.randint(1, 1000)), salt_length=12)
    return unique

