import time
from redis.asyncio import Redis


client = Redis(host='textai-redis')
pipeline = client.pipeline()


async def ratelimit(identifier: str, duration: int, num_of_requests: int) -> bool:
    key = f"ratelimit:{identifier}:{duration}"
    t = time.time()
    pipeline.zremrangebyscore(key, min=0, max=t - duration)
    pipeline.zcount(key, min=0, max=t)
    _, count = await pipeline.execute()
    if count >= num_of_requests:
        return False
    pipeline.zadd(key, {t: t})
    pipeline.expire(key, duration)
    await pipeline.execute()
    return True
