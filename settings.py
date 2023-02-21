from pydantic import BaseSettings


class Config(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_BASE: str
    DB_HOST: str
    DB_PORT: str

    SYNC_SQLALCHEMY_URL: str
    ASYNC_SQLALCHEMY_URL: str
    TEST_DATABASE_URL: str = 'postgresql://test:test@localhost:5432/test'

    SECRET = 'SECRET'
    TEST_PASSWORD: str

    TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = 'HS256'

    class Config:
        env_file = '.env'


config = Config()
