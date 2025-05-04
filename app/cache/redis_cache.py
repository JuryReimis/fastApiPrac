import json
from datetime import datetime
from functools import wraps
from typing import Optional

from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.redis import RedisCacheConfigSchema


class RedisCache:
    def __init__(self, config: RedisCacheConfigSchema):
        self._client = Redis(
            host=config.host,
            port=config.port,
            decode_responses=True
        )
        self.default_ttl = config.default_ttl

    async def clear_all(self):
        """Полная очистка кэша"""
        await self._client.flushdb()
        print(f"Кэш очищен: {datetime.now().isoformat()}")

    def cache(
            self,
            ttl: Optional[int] = None,
    ):
        """
        Декоратор для кэширования результатов функции

        :param ttl: Время жизни кэша в секундах (None - использовать default_ttl)
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_kwargs = {
                    k: v for k, v in kwargs.items()
                    if not isinstance(v, AsyncSession)
                }

                cache_key = f"cache:{func.__module__}:{func.__name__}:{cache_kwargs}"

                # Пробуем получить из кэша
                if cached := await self._client.get(cache_key):
                    try:
                        if hasattr(func, '__annotations__') and issubclass(func.__annotations__.get('return'),
                                                                           BaseModel):
                            print(f"Получено из кэша {cache_key}")
                            return func.__annotations__['return'].model_validate_json(cached)
                        return json.loads(cached)
                    except json.JSONDecodeError:
                        return cached.decode()

                result = await func(*args, **kwargs)

                # Сериализуем результат
                if isinstance(result, BaseModel):
                    serialized = result.model_dump_json().encode()
                else:
                    serialized = json.dumps(result).encode()

                # Сохраняем в Redis
                await self._client.set(
                    cache_key,
                    serialized,
                    ex=ttl or self.default_ttl
                )
                print(f"Сохранено в кэш по ключу {cache_key}")

                return result
            return wrapper
        return decorator
