import asyncio
import time

from redis.asyncio import Redis


client = Redis(host="textai-redis")


async def _ratelimit_helper(
    key: str, duration: int, n: int, t: float
) -> tuple[bool, float | None]:
    pipeline = client.pipeline()
    pipeline.zremrangebyscore(key, min=0, max=t - duration)
    pipeline.zcount(key, min=0, max=t)
    pipeline.zrange(key, 0, 0)
    _, count, scores = await pipeline.execute()
    if count >= n:
        lowest_score = float(scores[0])
        retry_after = duration - (t - lowest_score)
        return False, retry_after
    return True, None


async def _add_timestamp(key: str, duration: int, t: float):
    pipeline = client.pipeline()
    pipeline.zadd(key, {t: t})
    pipeline.expire(key, duration)
    await pipeline.execute()


async def ratelimit(identifier: str, duration: int, n: int) -> tuple[bool, float]:
    key = f"ratelimit:{identifier}:{duration}"
    t = time.time()

    success, retry_after = await _ratelimit_helper(key, duration, n, t)
    if success:
        await _add_timestamp(key, duration, t)

    return success, retry_after


async def multi_ratelimit(identifier: str, mapping: dict[int, int]):
    t = time.time()
    coroutines = []
    for duration, n in mapping.items():
        key = f"ratelimit:{identifier}:{duration}"
        coroutines.append(_ratelimit_helper(key, duration, n, t))

    results = await asyncio.gather(*coroutines)
    if not all([success for success, _, in results]):
        retry_after = max(
            [retry_after for _, retry_after in results if retry_after is not None]
        )
        return False, retry_after

    for duration, _ in mapping.items():
        key = f"ratelimit:{identifier}:{duration}"
        await _add_timestamp(key, duration, t)
    return True, None
