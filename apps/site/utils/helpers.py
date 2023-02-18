import hashlib
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError

from apps.site.schemas.user_schemas import UserCreate
from database.db_connection import db
from settings import config


def get_hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hash_pass


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    return get_hash_password(password) == hashed_password


def create_token(data: dict) -> tuple:
    """Create token for user"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=to_encode.get("expire_minutes")
    )
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET, algorithm=config.ALGORITHM
    )
    return encoded_jwt, expire


def decode_token(token: str) -> dict | str:
    try:
        data = jwt.decode(token, config.SECRET, algorithms=[config.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong token or it has expired",
        )
    return data


async def create_user(user: UserCreate):
    """Create new user."""
    hashed_password = get_hash_password(user.password)
    query = """
        INSERT INTO users VALUES (DEFAULT, :name, :password, :email)
        """
    await db.execute(
        query,
        {
            'name': user.name,
            'password': hashed_password,
            'email': user.email
        }
    )
    return {"status": "Success", "msg": "The user was created successfully"}


async def get_user_by_email(email: str):
    """Return user info by email."""
    query = """
        SELECT * FROM users
        WHERE email = :email
        """
    user = await db.fetch_one(query, {'email': email})
    if not user:
        return None
    return dict(user._mapping)


async def create_post(user_id: int, data: dict) -> None:
    """Add post into the database"""
    data["user_id"] = user_id
    query = """
        INSERT INTO posts VALUES (DEFAULT, :title, :text, :user_id);
        """
    await db.execute(query=query, values=data)


async def get_posts() -> list:
    """Get all posts from the database"""
    query = """
        SELECT * FROM posts;
        """
    posts = await db.fetch_all(query=query)
    return posts


async def delete_post(user_id: int, post_id: int):
    """Delete post from the database"""
    query = """
            DELETE FROM posts
            WHERE id = :post_id and user_id = :user_id
            RETURNING id;
            """
    post = await db.fetch_one(
        query=query, values={"post_id": post_id, "user_id": user_id}
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have such post",
        )


async def change_post(user_id, post_data: dict) -> None:
    set_list = []
    for field, value in post_data.copy().items():
        if value and field != 'id':
            set_list.append(f'{field} = :{field}')
        elif not value:
            del post_data[field]
    post_data.update({'user_id': user_id})
    query = f"""
        UPDATE posts
        SET {', '.join(set_list)}
        WHERE user_id = :user_id AND id = :id;
        """
    await db.execute(query=query, values=post_data)


async def check_owner(user_id: int, post_id: int) -> bool:
    query = """
        SELECT * FROM posts WHERE user_id = :user_id and id = :post_id
        """
    post = await db.fetch_one(
        query=query, values={'user_id': user_id, 'post_id': post_id}
    )
    if post:
        return True
    return False


async def get_rate(user_id: int, post_id: int) -> dict | None:
    select_query = """
        SELECT * FROM rates WHERE user_id = :user_id AND post_id = :post_id
        """
    rate_info = await db.fetch_one(
        query=select_query, values={'user_id': user_id, 'post_id': post_id}
    )
    if rate_info:
        return dict(rate_info._mapping)


async def set_rate(user_id: int, post_id: int, rate: str):
    if await check_owner(user_id, post_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't rate your own post",
        )
    final_data = {
        'user_id': user_id, 'post_id': post_id,
        'like': False, 'dislike': False
    }
    rate_info = await get_rate(user_id, post_id)
    if rate_info:
        if rate_info[rate] is True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You already {rate}d the post",
            )
        else:
            if rate == 'like':
                final_data['like'] = True
            else:
                final_data['dislike'] = True
            update_query = """
                UPDATE rates
                SET "like" = :like, dislike = :dislike
                WHERE user_id = :user_id AND post_id = :post_id
                """
            await db.execute(query=update_query,
                             values=final_data)
    else:
        final_data[rate] = True
        query = """
            INSERT INTO rates VALUES (:user_id, :post_id, :like, :dislike)
            """
        await db.execute(query=query, values=final_data)


async def delete_rate(user_id: int, post_id: int):
    query = """
        DELETE FROM rates 
        WHERE user_id = :user_id AND post_id = :post_id 
        RETURNING *
        """
    rate = await db.fetch_one(
        query=query, values={'user_id': user_id, 'post_id': post_id}
    )
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven't rated this post yet",
        )
