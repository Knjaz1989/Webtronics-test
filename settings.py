from pydantic import BaseSettings


class Config(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_BASE: str
    DB_HOST: str
    DB_PORT: str
    SQLALCHEMY_URL: str
    ASYNC_SQLALCHEMY_URL: str

    SECRET = 'SECRET'

    TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = 'HS256'

    class Config:
        env_file = '.env'


config = Config()
