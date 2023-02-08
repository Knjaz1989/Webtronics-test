import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    login = sa.Column(sa.VARCHAR(40), unique=True)
    password = sa.Column(sa.VARCHAR(100))
    email = sa.Column(sa.VARCHAR(100), unique=True)

    def __str__(self):
        return f'{self.login}: {self.email}'

    def __repr__(self):
        return f'{self.login}: {self.email}'


class Post(Base):
    __tablename__ = 'post'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    text = sa.Column(sa.TEXT)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    likes = sa.Column(sa.Integer, default=0)
    dislikes = sa.Column(sa.Integer, default=0)

    def __str__(self):
        return f'{self.login}: {self.email}'

    def __repr__(self):
        return f'{self.login}: {self.email}'
