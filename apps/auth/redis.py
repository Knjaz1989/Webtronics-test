import hashlib

import aioredis


async def get_redis():
    redis = await aioredis.from_url('redis://localhost/0')
    yield redis
    redis.close()


def get_hash_token(token: str) -> str:
    hash_token = hashlib.sha512(token.encode("utf-8")).hexdigest()
    return hash_token
