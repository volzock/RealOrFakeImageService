from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.redis_conn import redis_pool
from src.config import Config
from src.routers import service_routers

from src.database import init_db

if __name__ == '__main__':

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield
        await redis_pool.disconnect()

    app = FastAPI(title="Generated image detection service", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in service_routers:
        app.include_router(router)

    uvicorn.run(app, host=Config.HOST, port=Config.PORT)