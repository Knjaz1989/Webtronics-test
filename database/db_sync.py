from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import config


engine = create_engine(config.SYNC_SQLALCHEMY_URL)
Session = sessionmaker(bind=engine)
db = Session()
