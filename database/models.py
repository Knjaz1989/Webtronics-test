import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

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

    def __str__(self):
        return f'{self.login}: {self.email}'


class Rates(Base):
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
