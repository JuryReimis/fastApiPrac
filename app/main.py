from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.cache.sheduler_tasks import SchedulerTasks
from app.views import trading_views


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем планировщик при старте
    scheduler = SchedulerTasks()
    scheduler.make_clear_cache_task()

    yield

    # Остановка планировщика при завершении
    scheduler.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)

app.include_router(trading_views.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

