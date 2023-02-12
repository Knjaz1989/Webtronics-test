from databases import Database

from settings import config


DATABASE_URL = config.ASYNC_SQLALCHEMY_URL

db = Database(DATABASE_URL)
