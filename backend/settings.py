from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Config(BaseSettings):
    DEBUG_SERVER: bool = False

    DB_USER: str
    DB_PASSWORD: str
    DB_BASE: str
    DB_HOST: str
    DB_PORT: str

    SYNC_SQLALCHEMY_URL: str
    ASYNC_SQLALCHEMY_URL: str
    TEST_DATABASE_URL: str
    TEST_ASYNC_SQLALCHEMY_URL: str

    REDIS_URL: str

    HUNTER_API_KEY: str

    SECRET = 'SECRET'
    TEST_PASSWORD: str

    TOKEN_EXPIRE_SECONDS: int = 3600
    ALGORITHM: str = 'HS256'

    POSTS_LIMIT: int = 15
    POSTS_LIMIT_MAX: int = Field(30, ge=POSTS_LIMIT)
    POSTS_LIMIT_MIN: int = Field(1, ge=1, le=POSTS_LIMIT)

    class Config:
        env_file = '.env'


config = Config()
