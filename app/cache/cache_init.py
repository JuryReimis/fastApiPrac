from app.config import settings
from app.cache.redis_cache import RedisCache
from app.schemas.redis import RedisCacheConfigSchema


class RedisCacheService:
    cache = None

    @classmethod
    def init_cache(cls):
        cache_service = RedisCache(config=RedisCacheConfigSchema(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        ))
        cls.cache = cache_service
        return cls.cache

    @classmethod
    def get_cache_service(cls):
        if cls.cache is None:
            return cls.init_cache()
        return cls.cache



