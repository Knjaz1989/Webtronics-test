import click


@click.group("db")
def db_group():
    """Work with db"""


@db_group.command()
@click.argument('path')
def load_test_data(path: str):
    """Load test data to the database"""
    import hashlib
    import json

    from database.db_sync import db
    from database.models import User, Post

    from settings import config


    with open(path) as file:
        data = json.load(file)
    for item in data:
        user = User(
            name=item.get('name'),
            email=item.get('email'),
            hashed_password=hashlib.sha512(
                config.TEST_PASSWORD.encode("utf-8")
            ).hexdigest()
        )
        db.add(user)
        for post_item in item.get('posts', []):
            post = Post(
                title=post_item.get('title'),
                content=post_item.get('content')
            )
            post.user = user
            db.add(post)
    db.commit()

    print(data)
