from typing import Annotated

from pydantic import BaseModel, Field, RedisDsn


class RedisCacheConfigSchema(BaseModel):
    host: Annotated[str, Field(description="Хост Redis")] = 'localhost'
    port: Annotated[int, Field(description="Порт Redis")] = 6379
    dsn: Annotated[RedisDsn | None, Field(description="URL подключения (redis://...)")] = None
    default_ttl: Annotated[int | None, Field(description="TTL по умолчанию (секунды)")] = None
