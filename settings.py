import os

# from dotenv import load_dotenv
from pydantic import BaseSettings


# load_dotenv()


class Config(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_BASE: str
    DB_HOST: str
    DB_PORT: str
    SQLALCHEMY_URL: str
    ASYNC_SQLALCHEMY_URL: str

    SECRET = 'SECRET'

    class Config:
        env_file = '.env'


config = Config()
a = 1
