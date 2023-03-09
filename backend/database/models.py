from hashlib import sha512

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database.db_sync import Session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)
    hashed_password = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(50), unique=True, index=True, nullable=False)
    is_admin = sa.Column(
        sa.Boolean, server_default=sa.text('false'), nullable=False
    )
    rates = relationship("Rate", backref="user", uselist=True)

    def __str__(self):
        return f'{self.name}: {self.email}'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def sha512_password(cls, password: str) -> str:
        return sha512(password.encode('utf-8')).hexdigest()

    @classmethod
    def check_user(cls, email: str, password: str) -> 'User':
        with Session() as session:
            user = session.query(User).filter(
                User.email == email,
                User.hashed_password == cls.sha512_password(password)
            ).first()
            return user


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column(sa.VARCHAR(150))
    content = sa.Column(sa.TEXT)
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = relationship("User", backref="posts")
    rates = relationship("Rate", backref="post", lazy='dynamic')

    def __str__(self):
        return f'{self.login}: {self.email}'

    @hybrid_property
    def like_count(self) -> int:
        return self.rates.filter(Rate.like == True).count()

    @like_count.inplace.expression
    def like_count(cls):
        return sa.select(sa.func.count()).select_from(Rate).\
            where(sa.and_(
            Rate.post_id == cls.id, Rate.like == True
        ))

    @hybrid_property
    def dislike_count(self) -> int:
        return self.rates.filter(Rate.dislike == True).count()

    @dislike_count.inplace.expression
    def dislike_count(cls):
        return sa.select(sa.func.count()).select_from(Rate).\
            where(sa.and_(
            Rate.post_id == cls.id, Rate.dislike == True
        ))


class Rate(Base):
    __tablename__ = 'rates'

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    post_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True
    )
    like = sa.Column(sa.Boolean, server_default=sa.sql.text('false'))
    dislike = sa.Column(sa.Boolean, server_default=sa.text('false'))

    def __str__(self):
        return f'user: {self.user_id} - post: {self.post_id}'
