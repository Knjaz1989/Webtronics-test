from database.db_async import db


async def create_user(
    user_name: str, hashed_password: str, email: str
) -> None:
    """Add user into the database"""
    query = """
        INSERT INTO users VALUES (DEFAULT, :name, :hashed_password, :email);
        """
    await db.execute(
        query=query,
        values={
            'name': user_name, 'hashed_password': hashed_password,
            'email': email
        }
    )


async def delete_user(user_id: int) -> None:
    """Delete user from the database"""
    query = """
        DELETE FROM users WHERE id = :id;
        """
    await db.execute(query=query, values={'id': user_id})


async def get_user_by_email(email: str) -> dict | None:
    """Get user from the database by email"""
    query = """
        SELECT * FROM users WHERE email = :email;
        """
    user = await db.fetch_one(query=query, values={'email': email})
    if user:
        return dict(user._mapping)
