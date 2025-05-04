from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.cache.cache_init import RedisCacheService


class SchedulerTasks:

    def __init__(self):
        self._scheduler: AsyncIOScheduler | None = None

    def make_clear_cache_task(self):
        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_job(
            RedisCacheService.get_cache_service().clear_all,
            trigger=CronTrigger(hour=14, minute=11),
            name='clear_redis_cache'
        )
        self._scheduler.start()

    def shutdown(self, **kwargs):
        if self._scheduler is not None:
            self._scheduler.shutdown(**kwargs)
