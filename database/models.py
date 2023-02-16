import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)
    hashed_password = sa.Column(sa.String(), nullable=False)
    email = sa.Column(sa.String(50), unique=True, index=True)
    is_active = sa.Column(
        sa.Boolean,
        server_default=sa.sql.expression.true(),
        nullable=False,
    )

    def __str__(self):
        return f'{self.login}: {self.email}'

    def __repr__(self):
        return f'{self.login}: {self.email}'


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column(sa.VARCHAR(150))
    text = sa.Column(sa.TEXT)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id, ondelete='CASCADE'))
    likes = sa.Column(sa.Integer, server_default=sa.text('0'))
    dislikes = sa.Column(sa.Integer, server_default=sa.text('0'))

    def __str__(self):
        return f'{self.login}: {self.email}'

    def __repr__(self):
        return f'{self.login}: {self.email}'
