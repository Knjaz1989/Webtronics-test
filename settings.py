import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    base = os.getenv('DB_BASE')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    sqlalchemy_url = f"postgresql://{user}:{password}@{host}:{port}/{base}"


config = Config()
