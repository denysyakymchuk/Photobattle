from fastapi import FastAPI
from fastapi.security import HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.sessions import SessionMiddleware

SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/photo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY = "20"
ALGORITHM = "HS256"

Base = declarative_base()


security = HTTPBearer()

Base.metadata.create_all(bind=engine)


