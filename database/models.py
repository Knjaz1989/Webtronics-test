import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)
    hashed_password = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(50), unique=True, index=True, nullable=False)

    def __str__(self):
        return f'{self.name}: {self.email}'


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column(sa.VARCHAR(150))
    content = sa.Column(sa.TEXT)
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = relationship("User", backref="posts")
    rates = relationship("Rate", backref="post", uselist=True)

    def __str__(self):
        return f'{self.login}: {self.email}'

    @hybrid_property
    def like_count(self) -> int:
        count = 0
        for rate in self.rates:
            if rate.like is True:
                count += 1
        return count

    @like_count.inplace.expression
    def like_count(cls):
        return sa.select(sa.func.count()).select_from(Rate).\
            where(Rate.post_id == cls.id, Rate.like == True)

    @hybrid_property
    def dislike_count(self) -> int:
        count = 0
        for rate in self.rates:
            if rate.dislike is True:
                count += 1
        return count

    @dislike_count.inplace.expression
    def dislike_count(cls):
        return sa.select(sa.func.count()).select_from(Rate).\
            where(Rate.post_id == cls.id, Rate.dislike == True)


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
    user = relationship("User", backref="rates", uselist=True)

    def __str__(self):
        return f'user: {self.user_id} - post: {self.post_id}'
