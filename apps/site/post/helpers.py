from database.db_connection import db


async def create_post(user_id: int, data: dict) -> None:
    data["user_id"] = user_id
    query = """
        INSERT INTO posts VALUES (DEFAULT, :title, :text, :user_id)
        """
    await db.execute(query=query, values=data)
