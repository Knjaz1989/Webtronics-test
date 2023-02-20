from database.db_connection import db


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


async def create_post(user_id: int, title: str, content: str) -> None:
    """Add post into the database"""
    query = """
        INSERT INTO posts VALUES (DEFAULT, :title, :content, :user_id);
        """
    await db.execute(
        query=query,
        values={'user_id': user_id, 'title': title, 'content': content}
    )


async def get_user_by_email(email: str) -> dict | None:
    """Get user from the database by email"""
    query = """
        SELECT * FROM users WHERE email = :email;
        """
    user = await db.fetch_one(query=query, values={'email': email})
    if user:
        return dict(user._mapping)


async def delete_post(user_id: int, post_id: int) -> dict | None:
    """Delete post from the database"""
    query = """
        DELETE FROM posts
        WHERE id = :post_id and user_id = :user_id
        RETURNING *;
        """
    post = await db.fetch_one(
        query=query, values={'user_id': user_id, 'id': post_id}
    )
    if post:
        return dict(post._mapping)


async def change_post(
        post_id: int, title: str = None, content: str = None
):
    """Change current post in the database"""
    set_list = []
    values = {'title': title, 'content': content}
    for key, value in values.copy().items():
        if value:
            set_list.append(f'{key} = :{key}')
        else:
            del values[key]
    if not set_list:
        return
    values['id'] = post_id
    query = f"""
        UPDATE posts 
        SET {', '.join(set_list)}
        WHERE id = :id;
        """
    await db.execute(query=query, values=values)


async def get_post(post_id: int) -> dict | None:
    """Get current post from the database"""
    query = """
        SELECT * FROM posts WHERE id = :id;
        """
    post = db.fetch_one(query=query, values={'id': post_id})
    if post:
        return dict(post._mapping)


async def get_posts():
    """Get all posts from the database"""
    query = """
        SELECT * FROM posts;
        """
    posts = await db.fetch_all(query=query)
    return posts


async def get_ids_of_all_users_posts(user_id: int):
    pass


async def search_posts(title: str = None, content: str = None):
    """Search posts from the database"""
    select_list = []
    values = {'title': title, 'content': content}
    new_values = {}
    for key, value in values.items():
        if value:
            select_list.append(
                f"STRING_TO_ARRAY(LOWER({key}), ' ') && ARRAY[:{key}]"
            )
            new_values[key] = value
    query = f"""
        SELECT id, title, content FROM posts WHERE {' AND '.join(select_list)}; 
        """
    posts = await db.fetch_all(query=query, values=new_values)
    return posts
