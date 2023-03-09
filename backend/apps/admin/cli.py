import hashlib
import sys

import click
from sqlalchemy import text

from database.db_sync import Session


@click.group('admin')
def admin_group():
    """Work with admin"""


@admin_group.command()
def create_admin():
    with Session() as session:
        name = input('Please, enter admin name: ')
        email = input('Please, enter admin email: ')
        stmt = text(
            """
            SELECT * FROM users WHERE email = :email
            """
        )
        user = session.execute(stmt, {'email': email}).first()
        if user:
            sys.exit('There is such email in the database')
        password = hashlib.sha512(
            input('Введите пароль: ').encode('utf-8')
        ).hexdigest()
        stmt = text(
            """
            INSERT INTO users VALUES (DEFAULT, :name, :pass, :email, :is_a)
            RETURNING *;
            """
        )
        result = session.execute(
            stmt,
            {'name': name, 'pass': password, 'email': email, 'is_a': True}
        ).first()
        if not result:
            sys.exit('Someting wrong')
        print('The admin was created successfully')
        session.commit()
