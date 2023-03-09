import hashlib

import aioredis

from settings import config


async def get_redis():
    redis = await aioredis.from_url(config.REDIS_URL)
    yield redis
    await redis.close()


def get_hash_token(token: str) -> str:
    hash_token = hashlib.sha512(token.encode("utf-8")).hexdigest()
    return hash_token
