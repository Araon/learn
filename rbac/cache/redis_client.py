from redis import asyncio as aioredis

from core.config import settings

redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
